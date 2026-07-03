# pyright: reportOptionalSubscript=false
# pyright: reportOptionalMemberAccess=false
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from config.state import TELEGRAM_FILTER

WORDS_OPTIONS, SEE_WORDS, SET_WORDS = range(3)

async def words(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [InlineKeyboardButton('Ver Palavras', callback_data=SEE_WORDS)],
        [InlineKeyboardButton('Setar Palavras', callback_data=SET_WORDS)],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('<b>Escolha uma opção:</b>', parse_mode='HTML', reply_markup=reply_markup)

    return WORDS_OPTIONS


async def words_options(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    decision = int(query.data) # type: ignore

    if decision == SEE_WORDS:
        await query.edit_message_text(f"Palavras atualmente ativas: {TELEGRAM_FILTER.get_words()}")
    elif decision == SET_WORDS:
        await query.edit_message_text("Envia as palavras que deseja setar separadas por ';'.")
        return SET_WORDS
    

    return ConversationHandler.END


async def set_words(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_text = update.message.text

    words_list = [w.strip().lower() for w in user_text.split(';') if w.strip()]
    TELEGRAM_FILTER.set_words(words_list) 

    await update.message.reply_text("Palavras atualizadas com sucesso!")

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Ate mais"
    )

    return ConversationHandler.END



words_handler = ConversationHandler(
    entry_points=[CommandHandler('words', words)],
    states={
        WORDS_OPTIONS: [CallbackQueryHandler(words_options)],
        SET_WORDS: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_words)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)