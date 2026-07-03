# pyright: reportOptionalSubscript=false
# pyright: reportOptionalMemberAccess=false
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, ConversationHandler

MENU = 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands_text = (
        r"🤖 *Comandos Disponíveis:*" "\n\n"
        r"🔹 `/words` \- Manipular as palavras filtradas" "\n"
        r"🔹 `/channels` \- Manipular quais canais devem ser ouvidos" "\n\n"
        r"💡 _Dica: Digite /cancel a qualquer momento para sair\._"
    )
    await update.message.reply_text(commands_text, parse_mode='MarkdownV2')

    return MENU


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Ate mais"
    )

    return ConversationHandler.END

start_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        MENU: []
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)