import logging

from telegram import Update, PhotoSize, Document
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def image_handler(update: Update, context: CallbackContext) -> None:
    photo: PhotoSize = update.message.photo[-1]
    # This is the url which you can later you to download the image
    file_path: str = photo.get_file().file_path
    update.message.reply_text('file_path')


def document_image_handler(update: Update, context: CallbackContext) -> None:
    document: Document = update.message.document
    # This is the url which you can later use to download the image
    document_path: str = document.get_file().file_path
    update.message.reply_text('document_path')


def default(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('I don\'t really know how to respond to that. I think you should try the /help command.')


def main(token) -> None:
    updater = Updater(token)

    updater.dispatcher.add_handler(MessageHandler(Filters.photo, image_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.document.image, document_image_handler))
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