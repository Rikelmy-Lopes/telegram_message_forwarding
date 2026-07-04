# pyright: reportOptionalSubscript=false
# pyright: reportOptionalMemberAccess=false
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from bot.utils.text import format_words_list
from config.state import TELEGRAM_FILTER

WORDS_OPTIONS, SEE_WORDS, ADD_WORDS, DELETE_WORDS, CANCEL = range(5)

keyboard = [
    [InlineKeyboardButton('Visualizar Palavras', callback_data=SEE_WORDS)],
    [InlineKeyboardButton('Adicionar Palavras', callback_data=ADD_WORDS)],
    [InlineKeyboardButton('Excluir Palavras', callback_data=DELETE_WORDS)],
    [InlineKeyboardButton('Sair', callback_data=CANCEL)],
]

reply_markup = InlineKeyboardMarkup(keyboard)

async def words_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('<b>Escolha uma opção:</b>', parse_mode='HTML', reply_markup=reply_markup)

    return WORDS_OPTIONS


async def words_options_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    decision = int(query.data) # type: ignore
    current_words = TELEGRAM_FILTER.get_words()

    if decision == SEE_WORDS:
        reply_text = f"Palavras atualmente ativas:\n{format_words_list(current_words)}"

        await query.edit_message_text(reply_text, parse_mode='HTML', reply_markup=reply_markup)

        return WORDS_OPTIONS
    
    elif decision == ADD_WORDS:
        await query.edit_message_text("Envie as palavras que deseja adicionar separadas por ponto e vírgula (;)." \
            "\n\n<b>Exemplo:</b>\n<code>promoção; grátis; desconto</code>", parse_mode='HTML')
        return ADD_WORDS
    
    elif decision == DELETE_WORDS:
        if not current_words:
            await query.edit_message_text("Não há palavras para deletar!", reply_markup=reply_markup)
            return WORDS_OPTIONS
        
        reply_text = (
            "🗑️ <b>Excluir Palavras</b>\n\n"
            "Envie o número das palavras que deseja remover separadas por <code>;</code>.\n\n"
            "<b>Exemplo:</b> <code>1;3;5</code>\n\n"
            f"<b>Lista atual:</b>\n{format_words_list(current_words)}"
            )
        
        await query.edit_message_text(reply_text, parse_mode='HTML')
        return DELETE_WORDS
    
    elif decision == CANCEL:
        await query.edit_message_text("Até mais!")
        return ConversationHandler.END
    

    return ConversationHandler.END


async def add_words_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_text = update.message.text or ""

    words_list = [w.strip().lower() for w in user_text.split(';') if w.strip()]

    if words_list:
        TELEGRAM_FILTER.add_words(words_list)
        reply_text = f"Palavras atualizadas com sucesso!\n<b>Lista atual:</b>\n{format_words_list(TELEGRAM_FILTER.get_words())}"
    else:
        reply_text = "Nenhuma palavra válida enviada."

    await update.message.reply_text(reply_text, parse_mode='HTML')
    await update.message.reply_text('<b>Escolha uma opção:</b>', parse_mode='HTML', reply_markup=reply_markup)
    return WORDS_OPTIONS


async def delete_words_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_text = update.message.text or ""
    current_words = TELEGRAM_FILTER.get_words()

    indexs = [int(w.strip()) for w in user_text.split(';') if w.strip().isdigit()]
    valid_indices = [i for i in indexs if i >= 0 and i < len(current_words)]

    if not valid_indices:
        reply_text = f"Error ao deletar as palavras! Envie os numeros novamente.\n<b>Lista atual:</b>\n{format_words_list(current_words)}"
        await update.message.reply_text(reply_text, parse_mode='HTML')
        return DELETE_WORDS

    TELEGRAM_FILTER.delete_words(indexs)

    await update.message.reply_text("As palavras selecionadas foram deletadas com sucesso! 🎉", parse_mode='HTML')
    await update.message.reply_text('<b>Escolha uma opção:</b>', parse_mode='HTML', reply_markup=reply_markup)
    return WORDS_OPTIONS


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Até mais!"
    )

    return ConversationHandler.END



words_handler = ConversationHandler(
    entry_points=[CommandHandler('words', words_command)],
    states={
        WORDS_OPTIONS: [CallbackQueryHandler(words_options_command)],
        ADD_WORDS: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_words_command)],
        DELETE_WORDS: [MessageHandler(filters.TEXT & ~filters.COMMAND, delete_words_command)],
    },
    fallbacks=[CommandHandler('cancel', cancel_command)]
)