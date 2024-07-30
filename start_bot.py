import json
import logging

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from openai_tools import reply

api_token = json.load(open("auth.json", 'rb'))["telegram_api_token"]

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# We are using only a single state in this bot
REPLY = 0

# Define start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text("hi I am an AI replica of Leonardo Da Vinci, tag me in a message, or call me by name, using \"Leo\" or \"Leonardo\", and I will reply to you")
    return REPLY # this will trigger the bot to be in reply state

# Define help command handler
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text("hi I am an AI replica of Leonardo Da Vinci, tag me in a message, or call me by name, using \"Leo\" or \"Leonardo\", and I will reply to you. Use the /start command to start chatting with me.")


async def bot_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    reply_text = reply(update.message.text)

    await update.message.reply_text(reply)


def main():

    application = Application.builder().token(api_token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start), CommandHandler("help", help_command)],
        states={
            REPLY: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot_reply), CommandHandler("help", help_command)],
        }
    )

    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()