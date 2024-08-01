import json
import logging

from telegram import Update
from telegram.ext import Application 
from telegram.ext import ConversationHandler 
from telegram.ext import CommandHandler 
from telegram.ext import ContextTypes 
from telegram.ext import MessageHandler 
from telegram.ext import filters

from openai_tools import reply

api_token = json.load(open("auth.json", 'rb'))["telegram_api_token"]

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

bot_names = ["@davinci_ai_telegram_bot", "Leo", "Leonardo"]

# We are using only a single state in this bot
REPLY = 0

# Define start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text("Hi I am an AI replica of Leonardo Da Vinci. I will reply to your messages if call me by name, using \"Leo\" or \"Leonardo\" or if you reply to my messages. To be able to chat with me a member of this chat has to send the /start command first.")
    
    logger.info(f"Got start message transitioning to REPLY state..")

    return REPLY # this will trigger the bot to be in reply state

# Define help command handler
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text("Hi I am an AI replica of Leonardo Da Vinci. I will reply to your messages if call me by name, using \"Leo\" or \"Leonardo\" or if you reply to my messages. Use the /start command to start chatting with me. To be able to chat with me a member of this chat has to send the /start command first")


# Define help command handler
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await update.message.reply_text("Hi sorry to see you go!")

    return ConversationHandler.END


async def bot_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    if update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id:
        
        reply_text = reply(update.message.text)

        logger.info(f"Someone replied to a message, replying..")

        await update.message.reply_text(reply_text)

    elif any(name.lower() in update.message.text.lower() for name in bot_names):

        reply_text = reply(update.message.text)

        logger.info(f"Getting a direct message, replying..")

        await update.message.reply_text(reply_text)


def main():

    application = Application.builder().token(api_token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start), CommandHandler("help", help_command)],
        states={
            REPLY: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot_reply), CommandHandler("help", help_command)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()