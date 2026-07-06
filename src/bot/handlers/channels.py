# pyright: reportOptionalSubscript=false
# pyright: reportOptionalMemberAccess=false
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, LinkPreviewOptions, Update
from telegram.ext import CallbackQueryHandler, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from bot.utils.text import format_text_list
from config.state import TELEGRAM_FILTER
from utils import is_valid_url

CHANNELS_OPTIONS, SEE_CHANNELS, ADD_CHANNELS, DELETE_CHANNELS, CANCEL = range(5)

keyboard = [
    [InlineKeyboardButton('Visualizar Canais', callback_data=SEE_CHANNELS)],
    [InlineKeyboardButton('Adicionar Canais', callback_data=ADD_CHANNELS)],
    [InlineKeyboardButton('Excluir Canais', callback_data=DELETE_CHANNELS)],
    [InlineKeyboardButton('Sair', callback_data=CANCEL)],
]
back_keyboard = [[InlineKeyboardButton('Voltar', callback_data=str(CHANNELS_OPTIONS))]]


reply_markup = InlineKeyboardMarkup(keyboard)
back_reply_markup = InlineKeyboardMarkup(back_keyboard)

link_preview_options = LinkPreviewOptions(is_disabled=True)


async def channels_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('<b>Escolha uma opção:</b>', parse_mode='HTML', reply_markup=reply_markup)

    return CHANNELS_OPTIONS


async def channels_options_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    decision = int(query.data) # type: ignore
    current_channels = TELEGRAM_FILTER.get_channels()

    if decision == CHANNELS_OPTIONS:
        await query.edit_message_text('<b>Escolha uma opção:</b>', parse_mode='HTML', reply_markup=reply_markup)
        return CHANNELS_OPTIONS

    if decision == SEE_CHANNELS:
        reply_text = f"Canais atualmente sendo monitorados:\n{format_text_list(current_channels)}"

        await query.edit_message_text(reply_text, parse_mode='HTML', reply_markup=reply_markup, link_preview_options=link_preview_options)

        return CHANNELS_OPTIONS
    
    elif decision == ADD_CHANNELS:
        await query.edit_message_text("Envie as canais que deseja adicionar separadas por ponto e vírgula (;)." \
            "\n\n<b>Exemplo:</b>\n<code>https://t.me/example1; https://t.me/example2; https://t.me/example3</code>", parse_mode='HTML', 
            reply_markup=back_reply_markup)
        return ADD_CHANNELS
    
    elif decision == DELETE_CHANNELS:
        if not current_channels:
            await query.edit_message_text("Não há canais para deletar!", reply_markup=reply_markup)
            return CHANNELS_OPTIONS
        
        reply_text = (
            "🗑️ <b>Excluir Canais</b>\n\n"
            "Envie o número dos canais que deseja remover separadas por <code>;</code>.\n\n"
            "<b>Exemplo:</b> <code>1;3;5</code>\n\n"
            f"<b>Lista atual:</b>\n{format_text_list(current_channels)}"
            )
        
        await query.edit_message_text(reply_text, parse_mode='HTML', reply_markup=back_reply_markup, link_preview_options=link_preview_options)
        return DELETE_CHANNELS
    
    elif decision == CANCEL:
        await query.edit_message_text("Até mais!")
        return ConversationHandler.END
    

    return ConversationHandler.END


async def add_channels_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_text = update.message.text or ""

    print(user_text)

    channels_list = [c.strip() for c in user_text.split(';') if c.strip() and is_valid_url(c.strip())]

    if channels_list:
        TELEGRAM_FILTER.add_channels(channels_list)
        reply_text = f"Canais atualizadas com sucesso!\n<b>Lista atual:</b>\n{format_text_list(TELEGRAM_FILTER.get_channels())}"
    else:
        reply_text = "Nenhuma canal válido enviado."

    await update.message.reply_text(reply_text, parse_mode='HTML', link_preview_options=link_preview_options)
    await update.message.reply_text('<b>Escolha uma opção:</b>', parse_mode='HTML', reply_markup=reply_markup)
    return CHANNELS_OPTIONS


async def delete_channels_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_text = update.message.text or ""
    current_channels = TELEGRAM_FILTER.get_channels()

    indexs = [int(w.strip()) for w in user_text.split(';') if w.strip().isdigit()]
    valid_indices = [i for i in indexs if i >= 0 and i < len(current_channels)]

    if not valid_indices:
        reply_text = f"Error ao deletar as canais! Envie os numeros novamente.\n<b>Lista atual:</b>\n{format_text_list(current_channels)}"
        await update.message.reply_text(reply_text, parse_mode='HTML', reply_markup=back_reply_markup, link_preview_options=link_preview_options)
        return DELETE_CHANNELS

    TELEGRAM_FILTER.delete_channels(indexs)

    await update.message.reply_text("Os canais selecionados foram deletadas com sucesso! 🎉", parse_mode='HTML')
    await update.message.reply_text('<b>Escolha uma opção:</b>', parse_mode='HTML', reply_markup=reply_markup)
    return CHANNELS_OPTIONS


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Até mais!"
    )

    return ConversationHandler.END



channels_handler = ConversationHandler(
    entry_points=[CommandHandler('channels', channels_command)],
    states={
        CHANNELS_OPTIONS: [CallbackQueryHandler(channels_options_command)],
        ADD_CHANNELS: [
            CallbackQueryHandler(channels_options_command),
            MessageHandler(filters.TEXT & ~filters.COMMAND, add_channels_command)
            ],
        DELETE_CHANNELS: [
            CallbackQueryHandler(channels_options_command),
            MessageHandler(filters.TEXT & ~filters.COMMAND, delete_channels_command)
            ],
    },
    fallbacks=[
        CommandHandler('channels', channels_command),
        CommandHandler('cancel', cancel_command)
        ]
)
