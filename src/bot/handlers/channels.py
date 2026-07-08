# pyright: reportOptionalSubscript=false
# pyright: reportOptionalMemberAccess=false
import logging
from client.utils.chat import Chat
import client.utils.user
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, LinkPreviewOptions, Update
from telegram.ext import CallbackQueryHandler, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from bot.utils.state import new_state
from bot.utils.text import format_chat_list, format_text_list
from config.state import TELEGRAM_FILTER

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class States:
    MENU = new_state()
    LIST_CHANNELS = new_state()
    ADD_CHANNELS = new_state()
    DELETE_CHANNELS = new_state()
    CANCEL = new_state()


KEYBOARD = [
    [InlineKeyboardButton('Visualizar Canais', callback_data=States.LIST_CHANNELS)],
    [InlineKeyboardButton('Adicionar Canais', callback_data=States.ADD_CHANNELS)],
    [InlineKeyboardButton('Excluir Canais', callback_data=States.DELETE_CHANNELS)],
    [InlineKeyboardButton('Sair', callback_data=States.CANCEL)],
]
BACK_KEYBOARD = [[InlineKeyboardButton('Voltar', callback_data=States.MENU)]]


REPLY_MARKUP = InlineKeyboardMarkup(KEYBOARD)
BACK_REPLY_MARKUP = InlineKeyboardMarkup(BACK_KEYBOARD)
LINK_PREVIEW_OPTIONS = LinkPreviewOptions(is_disabled=True)


temp_chats: list[Chat] = []


async def channels_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('<b>Escolha uma opção:</b>', parse_mode='HTML', reply_markup=REPLY_MARKUP)

    return States.MENU


async def add_channels_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_text = update.message.text or ""

    indexs = [int(i.strip()) for i in user_text.split(';') if i.strip().isdigit()]

    if indexs:
        from client.handlers.handlers import update_on_new_messages_handler

        chats: list[Chat] = []
        for i in indexs:
            chats.append(temp_chats[i])
        
        TELEGRAM_FILTER.add_chats(chats)

        update_on_new_messages_handler()

        reply_text = f"Canais atualizados com sucesso!\n<b>Lista atual:</b>\n{format_chat_list(TELEGRAM_FILTER.get_chats())}"
        logger.info(reply_text)
    else:
        reply_text = "Nenhuma canal válido enviado."

    await update.message.reply_text(reply_text, parse_mode='HTML', link_preview_options=LINK_PREVIEW_OPTIONS)
    await update.message.reply_text('<b>Escolha uma opção:</b>', parse_mode='HTML', reply_markup=REPLY_MARKUP)

    return States.MENU


async def delete_channels_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_text = update.message.text or ""
    current_chats = TELEGRAM_FILTER.get_chats()

    indexs = [int(i.strip()) for i in user_text.split(';') if i.strip().isdigit()]
    valid_indices = [i for i in indexs if i >= 0 and i < len(current_chats)]

    if not valid_indices:
        reply_text = f"Erro ao deletar as canais! Envie os numeros novamente.\n<b>Lista atual:</b>\n{format_chat_list(current_chats)}"
        await update.message.reply_text(reply_text, parse_mode='HTML', reply_markup=BACK_REPLY_MARKUP, link_preview_options=LINK_PREVIEW_OPTIONS)

        return States.DELETE_CHANNELS

    removed = TELEGRAM_FILTER.delete_chats(valid_indices)
    from client.handlers.handlers import update_on_new_messages_handler

    update_on_new_messages_handler()
    
    logger.info(f"Canais removidos:\n{format_text_list(removed)}")

    await update.message.reply_text("Os canais selecionados foram deletadas com sucesso! 🎉", parse_mode='HTML')
    await update.message.reply_text('<b>Escolha uma opção:</b>', parse_mode='HTML', reply_markup=REPLY_MARKUP)

    return States.MENU


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Até mais!"
    )

    return ConversationHandler.END


async def handle_menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    selected_option = int(query.data) # type: ignore
    current_chats = TELEGRAM_FILTER.get_chats()

    if selected_option == States.MENU:
        await query.edit_message_text('<b>Escolha uma opção:</b>', parse_mode='HTML', reply_markup=REPLY_MARKUP)
        
        return States.MENU

    if selected_option == States.LIST_CHANNELS:
        reply_text = f"Canais atualmente sendo monitorados:\n{format_chat_list(current_chats)}"
        await query.edit_message_text(reply_text, parse_mode='HTML', reply_markup=REPLY_MARKUP, link_preview_options=LINK_PREVIEW_OPTIONS)

        return States.MENU
    
    elif selected_option == States.ADD_CHANNELS:
        temp_chats = await client.utils.user.get_user_chats()

        reply_text = (
            "➕ <b>Adicionar Canais</b>\n\n"
            "Envie o número dos canais que deseja adicionar separadas por ponto e vírgula (;).\n\n"
            "<b>Exemplo:</b> <code>1;3;5</code>\n\n"
            f"Chats disponiveis:\n{format_chat_list(temp_chats)}"
        )
        await query.edit_message_text(reply_text, parse_mode='HTML', reply_markup=BACK_REPLY_MARKUP)
        
        return States.ADD_CHANNELS
    
    elif selected_option == States.DELETE_CHANNELS:
        if not current_chats:
            await query.edit_message_text("Não há canais para deletar!", reply_markup=REPLY_MARKUP)

            return States.MENU
        
        reply_text = (
            "🗑️ <b>Excluir Canais</b>\n\n"
            "Envie o número dos canais que deseja remover separadas por <code>;</code>.\n\n"
            "<b>Exemplo:</b> <code>1;3;5</code>\n\n"
            f"<b>Lista atual:</b>\n{format_chat_list(current_chats)}"
            )
        await query.edit_message_text(reply_text, parse_mode='HTML', reply_markup=BACK_REPLY_MARKUP, link_preview_options=LINK_PREVIEW_OPTIONS)

        return States.DELETE_CHANNELS
    
    elif selected_option == States.CANCEL:
        await query.edit_message_text("Até mais!")

        return ConversationHandler.END
    

    return ConversationHandler.END



channels_handler = ConversationHandler(
    entry_points=[CommandHandler('channels', channels_command)],
    states={
        States.MENU: [CallbackQueryHandler(handle_menu_selection)],
        States.ADD_CHANNELS: [
            CallbackQueryHandler(handle_menu_selection),
            MessageHandler(filters.TEXT & ~filters.COMMAND, add_channels_command)
            ],
        States.DELETE_CHANNELS: [
            CallbackQueryHandler(handle_menu_selection),
            MessageHandler(filters.TEXT & ~filters.COMMAND, delete_channels_command)
            ],
    },
    fallbacks=[
        CommandHandler('channels', channels_command),
        CommandHandler('cancel', cancel_command)
        ]
)
