import argparse
import logging
from os import getenv

from telegram import Update
from telegram.error import TelegramError
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from messageFormatter import format
from system import get_ip, ping
from twitter import Twitter

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

TELEGRAM_TWITTER_CONSUMER_KEY = getenv("TELEGRAM_TWITTER_CONSUMER_KEY")
TELEGRAM_TWITTER_CONSUMER_SECRET = getenv("TELEGRAM_TWITTER_CONSUMER_SECRET")
TELEGRAM_TWITTER_ACCESS_TOKEN = getenv("TELEGRAM_TWITTER_ACCESS_TOKEN")
TELEGRAM_TWITTER_TOKEN_SECRET = getenv("TELEGRAM_TWITTER_TOKEN_SECRET")

TELEGRAM_TWITTER_BOT_TOKEN = getenv("TELEGRAM_TWITTER_BOT_TOKEN")
TELEGRAM_TWITTER_USER_ID = getenv("TELEGRAM_TWITTER_USER_ID")

parser = argparse.ArgumentParser(
    description="Script to download files from Telegram Channel.")
parser.add_argument("--consumer-key",
                    required=TELEGRAM_TWITTER_CONSUMER_KEY == None,
                    type=str,
                    default=TELEGRAM_TWITTER_CONSUMER_KEY)
parser.add_argument("--consumer-secret",
                    required=TELEGRAM_TWITTER_CONSUMER_SECRET == None,
                    type=str,
                    default=TELEGRAM_TWITTER_CONSUMER_SECRET)
parser.add_argument("--access-token",
                    required=TELEGRAM_TWITTER_ACCESS_TOKEN == None,
                    type=str,
                    default=TELEGRAM_TWITTER_ACCESS_TOKEN)
parser.add_argument("--access-token-secret",
                    required=TELEGRAM_TWITTER_TOKEN_SECRET == None,
                    type=str,
                    default=TELEGRAM_TWITTER_TOKEN_SECRET)
parser.add_argument("--bot-token",
                    required=TELEGRAM_TWITTER_BOT_TOKEN == None,
                    type=str,
                    default=TELEGRAM_TWITTER_BOT_TOKEN)
parser.add_argument("--user-id",
                    required=False,
                    type=int,
                    default=TELEGRAM_TWITTER_USER_ID)
args = parser.parse_args()

consumer_key = args.consumer_key
consumer_secret = args.consumer_secret
access_token = args.access_token
access_token_secret = args.access_token_secret
bot_token = args.bot_token
user_id = args.user_id

if not user_id:
    logger.warning('user_id not set, you will not be able to tweet')

twitter = Twitter(consumer_key, consumer_secret, access_token,
                  access_token_secret)


def error_handler(update: Update, context: CallbackContext):
    try:
        raise context.error
    except TelegramError as e:
        update.message.reply_text(str(e))
        logger.exception(e)
    except Exception as e:
        update.message.reply_text(str(e))
        logger.exception(e)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def get_id(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text(update.effective_user.id)


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    if update.effective_user.id != user_id:
        update.message.reply_text("You are not authorized to use this bot.")
        return

    try:
        message = format(update.message.text)
        if message:
            twitter.status(message)
        update.message.reply_text(message or update.message.text)
        logger.info(message or update.message.text)

    except Exception as e:
        logger.exception(e)
        update.message.reply_text(str(e))


def command_ip(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id != user_id:
        update.message.reply_text("You are not authorized to use this bot.")
        return
    callback_ip(context)


def callback_ip(context: CallbackContext):
    try:
        message = f'IP: {get_ip()}'
        logger.info(message)
        context.bot.send_message(
            chat_id=user_id,
            text=message
        )
    except Exception as e:
        logger.exception(e)
        context.bot.send_message(
            chat_id=user_id,
            text=str(e)
        )


def command_ping(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id != user_id:
        update.message.reply_text("You are not authorized to use this bot.")
        return
    callback_ping(context)


def callback_ping(context: CallbackContext):
    try:
        message = f'Ping: {ping()}'
        logger.info(message)
        context.bot.send_message(
            chat_id=user_id,
            text=message
        )
    except Exception as e:
        logger.exception(e)
        context.bot.send_message(
            chat_id=user_id,
            text=str(e)
        )


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
    dispatcher.add_handler(CommandHandler("id", get_id))
    dispatcher.add_handler(CommandHandler("ip", command_ip))
    dispatcher.add_handler(CommandHandler("ping", command_ping))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, echo))

    dispatcher.add_error_handler(error_handler)

    jobQueue = updater.job_queue

    MINUTE = 60
    jobQueue.run_repeating(callback_ip, interval=MINUTE * 5, first=1)
    jobQueue.run_repeating(callback_ping, interval=MINUTE * 5, first=1)

    # Start the Bot
    updater.start_polling()

    logger.info('Bot is on')

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
