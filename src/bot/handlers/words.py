# pyright: reportOptionalSubscript=false
# pyright: reportOptionalMemberAccess=false
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from config.state import TELEGRAM_FILTER

WORDS_OPTIONS, SEE_WORDS, ADD_WORDS, DELETE_WORDS, CANCEL = range(5)

keyboard = [
    [InlineKeyboardButton('Visualizar Palavras', callback_data=SEE_WORDS)],
    [InlineKeyboardButton('Adicionar Palavras', callback_data=ADD_WORDS)],
    [InlineKeyboardButton('Excluir Palavras', callback_data=DELETE_WORDS)],
    [InlineKeyboardButton('Sair', callback_data=CANCEL)],
]

reply_markup = InlineKeyboardMarkup(keyboard)

def concatenate_words(text: str, words: list[str]):
    for index, word in enumerate(words):
        text += f"<b>{index}</b> - {word}\n"

    return text


async def words(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('<b>Escolha uma opção:</b>', parse_mode='HTML', reply_markup=reply_markup)

    return WORDS_OPTIONS


async def words_options(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    decision = int(query.data) # type: ignore

    if decision == SEE_WORDS:
        reply_text = "Palavras atualmente ativas:\n"
        reply_text = concatenate_words(reply_text, TELEGRAM_FILTER.get_words())

        await query.edit_message_text(reply_text, parse_mode='HTML')
    elif decision == ADD_WORDS:
        await query.edit_message_text("Envia as palavras que deseja adicionar separadas por ';'.")
        return ADD_WORDS
    elif decision == DELETE_WORDS:
        if len(TELEGRAM_FILTER.get_words()) == 0:
            await query.edit_message_text("Não ha palavras para deletar!")
            return ConversationHandler.END
        
        reply_text = "Envie o numero das palavras separadas por ';' que deseja deletar!\nPalavras:\n"
        reply_text = concatenate_words(reply_text, TELEGRAM_FILTER.get_words())
        
        await query.edit_message_text(reply_text, parse_mode='HTML')
        return DELETE_WORDS
    elif decision == CANCEL:
        await query.edit_message_text("Ate mais")
        return ConversationHandler.END
    

    return ConversationHandler.END


async def add_words(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_text = update.message.text

    words_list = [w.strip().lower() for w in user_text.split(';') if w.strip()]
    TELEGRAM_FILTER.add_words(words_list)

    reply_text = "Palavras atualizadas com sucesso!\nPalavras:\n"
    reply_text = concatenate_words(reply_text, TELEGRAM_FILTER.get_words())

    await update.message.reply_text(reply_text, parse_mode='HTML')

    await update.message.reply_text('<b>Escolha uma opção:</b>', parse_mode='HTML', reply_markup=reply_markup)

    return WORDS_OPTIONS


async def delete_words(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_text = update.message.text
    indexs = [int(w.strip()) for w in user_text.split(';') if w.strip().isdigit()]

    if len(indexs) == 0:
        reply_text = "Error ao deletar as palavras! Envie os numeros novamente.\nPalavras:\n"
        reply_text = concatenate_words(reply_text, TELEGRAM_FILTER.get_words())

        await update.message.reply_text(reply_text, parse_mode='HTML')

        return DELETE_WORDS

    TELEGRAM_FILTER.delete_words(indexs)

    await update.message.reply_text("Palavras deletadas com sucesso!")

    await update.message.reply_text('<b>Escolha uma opção:</b>', parse_mode='HTML', reply_markup=reply_markup)

    return WORDS_OPTIONS


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Ate mais"
    )

    return ConversationHandler.END



words_handler = ConversationHandler(
    entry_points=[CommandHandler('words', words)],
    states={
        WORDS_OPTIONS: [CallbackQueryHandler(words_options)],
        ADD_WORDS: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_words)],
        DELETE_WORDS: [MessageHandler(filters.TEXT & ~filters.COMMAND, delete_words)],
        CANCEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, cancel)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)