import logging

from telegram import Update
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def default(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('I don\'t really know how to respond to that. I think you should try the /help command.')


def main(token) -> None:
    updater = Updater(token)

    updater.dispatcher.add_handler(MessageHandler(Filters.all, default))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    with open('.token') as f:
        token = f.read()

    main(token)