# pyright: reportOptionalSubscript=false
# pyright: reportOptionalMemberAccess=false
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from bot.utils.state import new_state
from bot.utils.text import format_text_list
from config.state import TELEGRAM_FILTER

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class States:
    MENU = new_state()
    LIST_WORDS = new_state()
    ADD_WORDS = new_state()
    DELETE_WORDS = new_state()
    CANCEL = new_state()

KEYBOARD = [
    [InlineKeyboardButton('Visualizar Palavras', callback_data=States.LIST_WORDS)],
    [InlineKeyboardButton('Adicionar Palavras', callback_data=States.ADD_WORDS)],
    [InlineKeyboardButton('Excluir Palavras', callback_data=States.DELETE_WORDS)],
    [InlineKeyboardButton('Sair', callback_data=States.CANCEL)],
]
BACK_KEYBOARD = [[InlineKeyboardButton('Voltar', callback_data=States.MENU)]]

REPLY_MARKUP = InlineKeyboardMarkup(KEYBOARD)
BACK_REPLY_MARKUP = InlineKeyboardMarkup(BACK_KEYBOARD)


async def words_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('<b>Escolha uma opção:</b>', parse_mode='HTML', reply_markup=REPLY_MARKUP)

    return States.MENU


async def add_words_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_text = update.message.text or ""

    words_list = [w.strip().lower() for w in user_text.split(';') if w.strip()]

    if words_list:
        TELEGRAM_FILTER.add_words(words_list)
        reply_text = f"Palavras atualizadas com sucesso!\n<b>Lista atual:</b>\n{format_text_list(TELEGRAM_FILTER.get_words())}"
        logger.info(reply_text)
    else:
        reply_text = "Nenhuma palavra válida enviada."

    await update.message.reply_text(reply_text, parse_mode='HTML')
    await update.message.reply_text('<b>Escolha uma opção:</b>', parse_mode='HTML', reply_markup=REPLY_MARKUP)
    return States.MENU


async def delete_words_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_text = update.message.text or ""
    current_words = TELEGRAM_FILTER.get_words()

    indexs = [int(w.strip()) for w in user_text.split(';') if w.strip().isdigit()]
    valid_indices = [i for i in indexs if i >= 0 and i < len(current_words)]

    if not valid_indices:
        reply_text = f"Erro ao deletar as palavras! Envie os numeros novamente.\n<b>Lista atual:</b>\n{format_text_list(current_words)}"
        await update.message.reply_text(reply_text, parse_mode='HTML', reply_markup=BACK_REPLY_MARKUP)
        return States.DELETE_WORDS

    removed = TELEGRAM_FILTER.delete_words(valid_indices)
    logger.info(f"Palavras removidas:\n{format_text_list(removed)}")

    await update.message.reply_text("As palavras selecionadas foram deletadas com sucesso! 🎉", parse_mode='HTML')
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
    current_words = TELEGRAM_FILTER.get_words()

    if selected_option == States.MENU:
        await query.edit_message_text('<b>Escolha uma opção:</b>', parse_mode='HTML', reply_markup=REPLY_MARKUP)
        return States.MENU

    elif selected_option == States.LIST_WORDS:
        reply_text = f"Palavras atualmente ativas:\n{format_text_list(current_words)}"

        await query.edit_message_text(reply_text, parse_mode='HTML', reply_markup=REPLY_MARKUP)

        return States.MENU
    
    elif selected_option == States.ADD_WORDS:
        await query.edit_message_text("Envie as palavras que deseja adicionar separadas por ponto e vírgula (;)." \
            "\n\n<b>Exemplo:</b>\n<code>promoção; grátis; desconto</code>", parse_mode='HTML', reply_markup=BACK_REPLY_MARKUP)
        return States.ADD_WORDS
    
    elif selected_option == States.DELETE_WORDS:
        if not current_words:
            await query.edit_message_text("Não há palavras para deletar!", reply_markup=REPLY_MARKUP)
            return States.MENU
        
        reply_text = (
            "🗑️ <b>Excluir Palavras</b>\n\n"
            "Envie o número das palavras que deseja remover separadas por <code>;</code>.\n\n"
            "<b>Exemplo:</b> <code>1;3;5</code>\n\n"
            f"<b>Lista atual:</b>\n{format_text_list(current_words)}"
            )
        
        await query.edit_message_text(reply_text, parse_mode='HTML', reply_markup=BACK_REPLY_MARKUP)
        return States.DELETE_WORDS
    
    elif selected_option == States.CANCEL:
        await query.edit_message_text("Até mais!")
        return ConversationHandler.END
    

    return ConversationHandler.END



words_handler = ConversationHandler(
    entry_points=[CommandHandler('words', words_command)],
    states={
        States.MENU: [CallbackQueryHandler(handle_menu_selection)],
        States.ADD_WORDS: [
            CallbackQueryHandler(handle_menu_selection),
            MessageHandler(filters.TEXT & ~filters.COMMAND, add_words_command)
        ],
        States.DELETE_WORDS: [
            CallbackQueryHandler(handle_menu_selection),
            MessageHandler(filters.TEXT & ~filters.COMMAND, delete_words_command)
        ],
    },
    fallbacks=[
        CommandHandler('words', words_command),
        CommandHandler('cancel', cancel_command)
        ]
)