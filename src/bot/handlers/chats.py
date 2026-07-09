# pyright: reportOptionalSubscript=false
# pyright: reportOptionalMemberAccess=false
import logging
from client.utils.chat import Chat
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, LinkPreviewOptions, Update
from telegram.ext import CallbackQueryHandler, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from client.handlers.handlers import update_on_new_messages_handler
from client.utils.user import get_user_chats
from bot.utils.state import new_state
from utils.text import format_chat_list
from config.state import STATE

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

TELEGRAM_FILTER = STATE.get_telegram_filter()

class ConversationState:
    MENU = new_state()
    LIST_CHATS = new_state()
    ADD_CHATS = new_state()
    DELETE_CHATS = new_state()
    CANCEL = new_state()


KEYBOARD = [
    [InlineKeyboardButton('Visualizar Chats', callback_data=ConversationState.LIST_CHATS)],
    [InlineKeyboardButton('Adicionar Chats', callback_data=ConversationState.ADD_CHATS)],
    [InlineKeyboardButton('Excluir Chats', callback_data=ConversationState.DELETE_CHATS)],
    [InlineKeyboardButton('Sair', callback_data=ConversationState.CANCEL)],
]
BACK_KEYBOARD = [[InlineKeyboardButton('Voltar', callback_data=ConversationState.MENU)]]


REPLY_MARKUP = InlineKeyboardMarkup(KEYBOARD)
BACK_REPLY_MARKUP = InlineKeyboardMarkup(BACK_KEYBOARD)
LINK_PREVIEW_OPTIONS = LinkPreviewOptions(is_disabled=True)


temp_chats: list[Chat] = []


async def chats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('<b>Escolha uma opção:</b>', parse_mode='HTML', reply_markup=REPLY_MARKUP)

    return ConversationState.MENU


async def add_chats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_text = update.message.text or ""
    global temp_chats

    indexs = [int(i.strip()) for i in user_text.split(';') if i.strip().isdigit()]
    valid_indexs = [i for i in indexs if i >= 0 and i < len(temp_chats)]

    if valid_indexs:

        chats: list[Chat] = []
        for i in valid_indexs:
            chats.append(temp_chats[i])
        
        TELEGRAM_FILTER.add_chats(chats)

        update_on_new_messages_handler()

        reply_text = f"Chats atualizados com sucesso!\n<b>Lista atual:</b>\n{format_chat_list(TELEGRAM_FILTER.get_chats())}"
        logger.info(reply_text)
    else:
        reply_text = "Nenhuma chat válido enviado."

    await update.message.reply_text(reply_text, parse_mode='HTML', link_preview_options=LINK_PREVIEW_OPTIONS)
    await update.message.reply_text('<b>Escolha uma opção:</b>', parse_mode='HTML', reply_markup=REPLY_MARKUP)

    return ConversationState.MENU


async def delete_chats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_text = update.message.text or ""
    current_chats = TELEGRAM_FILTER.get_chats()

    indexs = [int(i.strip()) for i in user_text.split(';') if i.strip().isdigit()]
    valid_indices = [i for i in indexs if i >= 0 and i < len(current_chats)]

    if not valid_indices:
        reply_text = f"Erro ao deletar os chats! Envie os numeros novamente.\n<b>Lista atual:</b>\n{format_chat_list(current_chats)}"
        await update.message.reply_text(reply_text, parse_mode='HTML', reply_markup=BACK_REPLY_MARKUP, link_preview_options=LINK_PREVIEW_OPTIONS)

        return ConversationState.DELETE_CHATS

    removed = TELEGRAM_FILTER.delete_chats(valid_indices)

    update_on_new_messages_handler()
    
    logger.info(f"Chats removidos:\n{format_chat_list(removed)}")

    await update.message.reply_text("Os chats selecionados foram deletadas com sucesso! 🎉", parse_mode='HTML')
    await update.message.reply_text('<b>Escolha uma opção:</b>', parse_mode='HTML', reply_markup=REPLY_MARKUP)

    return ConversationState.MENU


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

    if selected_option == ConversationState.MENU:
        await query.edit_message_text('<b>Escolha uma opção:</b>', parse_mode='HTML', reply_markup=REPLY_MARKUP)
        
        return ConversationState.MENU

    if selected_option == ConversationState.LIST_CHATS:
        reply_text = f"Chats atualmente sendo monitorados:\n\n{format_chat_list(current_chats)}"
        await query.edit_message_text(reply_text, parse_mode='HTML', reply_markup=REPLY_MARKUP, link_preview_options=LINK_PREVIEW_OPTIONS)

        return ConversationState.MENU
    
    elif selected_option == ConversationState.ADD_CHATS:
        global temp_chats
        temp_chats = await get_user_chats()

        reply_text = (
            "➕ <b>Adicionar Chats</b>\n\n"
            "Envie o número dos chats que deseja adicionar separadas por ponto e vírgula (;).\n\n"
            "<b>Exemplo:</b> <code>1;3;5</code>\n\n"
            f"Chats disponiveis:\n{format_chat_list(temp_chats)}"
        )
        await query.edit_message_text(reply_text, parse_mode='HTML', reply_markup=BACK_REPLY_MARKUP)
        
        return ConversationState.ADD_CHATS
    
    elif selected_option == ConversationState.DELETE_CHATS:
        if not current_chats:
            await query.edit_message_text("Não há chats para deletar!", reply_markup=REPLY_MARKUP)

            return ConversationState.MENU
        
        reply_text = (
            "🗑️ <b>Excluir Chats</b>\n\n"
            "Envie o número dos chats que deseja remover separadas por <code>;</code>.\n\n"
            "<b>Exemplo:</b> <code>1;3;5</code>\n\n"
            f"<b>Lista atual:</b>\n{format_chat_list(current_chats)}"
            )
        await query.edit_message_text(reply_text, parse_mode='HTML', reply_markup=BACK_REPLY_MARKUP, link_preview_options=LINK_PREVIEW_OPTIONS)

        return ConversationState.DELETE_CHATS
    
    elif selected_option == ConversationState.CANCEL:
        await query.edit_message_text("Até mais!")

        return ConversationHandler.END
    

    return ConversationHandler.END



chats_handler = ConversationHandler(
    entry_points=[CommandHandler('chats', chats_command)],
    states={
        ConversationState.MENU: [CallbackQueryHandler(handle_menu_selection)],
        ConversationState.ADD_CHATS: [
            CallbackQueryHandler(handle_menu_selection),
            MessageHandler(filters.TEXT & ~filters.COMMAND, add_chats_command)
            ],
        ConversationState.DELETE_CHATS: [
            CallbackQueryHandler(handle_menu_selection),
            MessageHandler(filters.TEXT & ~filters.COMMAND, delete_chats_command)
            ],
    },
    fallbacks=[
        CommandHandler('chats', chats_command),
        CommandHandler('cancel', cancel_command)
        ]
)
