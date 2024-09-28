import logging
from telegram import Update
from telegram.ext import Application, CommandHandler

# Replace 'YOUR_TOKEN' with your actual bot token
BOT_TOKEN = '8186139630:AAE82j5EVSBK2LRGOTXZfZ8L2GuL5o_Fa9s'

# Enable logging for troubleshooting
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context):
    await update.message.reply_text('Welcome to HerSafeJourney Bot! Type /help to get started.')

async def help_command(update: Update, context):
    await update.message.reply_text('Available commands: /search [city] to find events.')

def main():
    # Create the Application and pass it the bot's token
    application = Application.builder().token(BOT_TOKEN).build()

    # Register the command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Start polling to receive updates from Telegram
    application.run_polling()

if __name__ == '__main__':
    main()
