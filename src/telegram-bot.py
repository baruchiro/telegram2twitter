import logging
from twitter import Twitter
from messageFormatter import format
from os import getenv
import argparse

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

TELEGRAM_TWITTER_CONSUMER_KEY = getenv("TELEGRAM_TWITTER_CONSUMER_KEY")
TELEGRAM_TWITTER_CONSUMER_SECRET = getenv("TELEGRAM_TWITTER_CONSUMER_SECRET")
TELEGRAM_TWITTER_ACCESS_TOKEN = getenv("TELEGRAM_TWITTER_ACCESS_TOKEN")
TELEGRAM_TWITTER_TOKEN_SECRET = getenv("TELEGRAM_TWITTER_TOKEN_SECRET")

TELEGRAM_TWITTER_BOT_TOKEN = getenv("TELEGRAM_TWITTER_BOT_TOKEN")

parser = argparse.ArgumentParser(
    description="Script to download files from Telegram Channel.")
parser.add_argument(
    "--consumer-key",
    required=TELEGRAM_TWITTER_CONSUMER_KEY == None,
    type=str,
    default=TELEGRAM_TWITTER_CONSUMER_KEY
)
parser.add_argument(
    "--consumer-secret",
    required=TELEGRAM_TWITTER_CONSUMER_SECRET == None,
    type=str,
    default=TELEGRAM_TWITTER_CONSUMER_SECRET
)
parser.add_argument(
    "--access-token",
    required=TELEGRAM_TWITTER_ACCESS_TOKEN == None,
    type=str,
    default=TELEGRAM_TWITTER_ACCESS_TOKEN
)
parser.add_argument(
    "--access-token-secret",
    required=TELEGRAM_TWITTER_TOKEN_SECRET == None,
    type=str,
    default=TELEGRAM_TWITTER_TOKEN_SECRET
)
parser.add_argument(
    "--bot-token",
    required=TELEGRAM_TWITTER_BOT_TOKEN == None,
    type=str,
    default=TELEGRAM_TWITTER_BOT_TOKEN
)
args = parser.parse_args()

consumer_key = args.consumer_key
consumer_secret = args.consumer_secret
access_token = args.access_token
access_token_secret = args.access_token_secret
bot_token = args.bot_token

twitter = Twitter(consumer_key, consumer_secret, access_token, access_token_secret)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    message = format(update.message.text)
    if message: twitter.status(message)
    update.message.reply_text(message or update.message.text)
    logger.info(message or update.message.text)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(bot_token, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    logger.info('Bot is on')

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()