import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater, 
    CommandHandler, 
    CallbackContext, 
    CallbackQueryHandler,
    MessageHandler,
    Filters,
    ConversationHandler
)

# Configuration
BOT_TOKEN = os.getenv('8194682764:AAHaEtntyLzlC3uujng9JSynVu4OnEv2Sj8')
CHANNEL_LINK = "https://t.me/Yakstaschannel"
GROUP_LINK = "https://t.me/yakstascapital"
TWITTER_LINK = "https://twitter.com/bigbangdist10"

# Conversation states
WAITING_WALLET = 1

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("✅ Submit Solana Wallet", callback_data="submit_wallet")]
    ]
    update.message.reply_text(
        f"🌟 *Welcome to mr kayblezzy2 Airdrop Program!* 🌟\n\n"
        f"To qualify:\n"
        f"1. Join our [Telegram channel]({CHANNEL_LINK})\n"
        f"2. Join our [Telegram group]({GROUP_LINK})\n"
        f"3. Follow our [Twitter]({TWITTER_LINK})\n\n"
        f"_This is a test bot - no actual SOL will be distributed_\n\n"
        f"Click below to submit your wallet:",
        parse_mode='Markdown',
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def submit_wallet(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        "🪙 *Please enter your Solana wallet address:*\n\n"
        "(Should be 32-44 characters long)",
        parse_mode='Markdown'
    )
    return WAITING_WALLET

def handle_wallet(update: Update, context: CallbackContext) -> int:
    wallet = update.message.text.strip()
    
    # Basic Solana address validation
    if 32 <= len(wallet) <= 44:
        update.message.reply_text(
            "🎉 *CONGRATULATIONS!*\n\n"
            "You passed mr kayblezzy2 airdrop call!\n\n"
            "💸 *100 SOL is on its way to your address!*\n\n"
            "⚠️ Hope you didn't cheat the system!\n\n"
            "_Note: This is a test bot - no actual SOL will be sent_",
            parse_mode='Markdown'
        )
        return ConversationHandler.END
    else:
        update.message.reply_text(
            "⚠️ Invalid Solana address format!\n"
            "Please enter a valid wallet address (32-44 characters):"
        )
        return WAITING_WALLET

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Submission cancelled.')
    return ConversationHandler.END

def main() -> None:
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            CallbackQueryHandler(submit_wallet, pattern='submit_wallet')
        ],
        states={
            WAITING_WALLET: [
                MessageHandler(Filters.text & ~Filters.command, handle_wallet)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler('start', start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
