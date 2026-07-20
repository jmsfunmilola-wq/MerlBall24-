import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get the bot token from environment variables
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    logger.error("No TELEGRAM_BOT_TOKEN found in environment variables!")
    raise ValueError("No TELEGRAM_BOT_TOKEN found in environment variables!")

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"🎯 Hello {user.first_name}! I'm MerlBall24Bot!\n\n"
        "I'm here to help you with whatever you need. Try these commands:\n"
        "/help - Show available commands\n"
        "/ping - Check if I'm alive\n"
        "/info - Get bot information"
    )

# Command: /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 Available Commands:\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/ping - Check if bot is alive\n"
        "/info - Get bot information\n\n"
        "💡 Just send me any message and I'll echo it back!"
    )

# Command: /ping
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 Pong! I'm alive and running smoothly!")

# Command: /info
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 MerlBall24Bot\n"
        "Version: 1.0.0\n"
        "Hosted on: Railway\n"
        "Made with: Python & python-telegram-bot\n\n"
        "🟢 Status: Online"
    )

# Handler for any text messages (echo)
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text:
        await update.message.reply_text(f"📨 You said: {update.message.text}")

# Handler for errors
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.message:
        await update.message.reply_text("⚠️ Something went wrong! Please try again later.")

# Main function
def main():
    logger.info("🚀 Starting MerlBall24Bot...")
    
    # Create the application
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("info", info))
    
    # Add echo handler for all text messages (excluding commands)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Add error handler
    app.add_error_handler(error_handler)
    
    # Start the bot using polling
    logger.info("✅ Bot is ready! Starting polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
