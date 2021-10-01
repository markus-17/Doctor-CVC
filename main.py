import logging

from telegram import Update, PhotoSize, Document, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters, CommandHandler, CallbackQueryHandler

import io
from PIL import Image


from pneumonia import predict as pneumonia_predict
from brain import predict as brain_predict

predict = {
    'pneumonia': pneumonia_predict,
    'brain': brain_predict
}


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def select_classifier_handler(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [ InlineKeyboardButton('Pneumonia Classifier', callback_data='pneumonia') ],
        [ InlineKeyboardButton('Brain Tumor Classifier', callback_data='brain') ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Choose One of the following models: ', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    query: CallbackQuery = update.callback_query
    user_id = query.from_user.id

    # The bot_data property is a dict that can be used to keep any data in.
    # For each update it will be the same
    context.bot_data[user_id] = query.data

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text=f"Selected option: {query.data}")


def image_handler(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    
    if user_id not in context.bot_data:
        update.message.reply_text('You have to select the classifier using the /classifier command.')
        return

    photo: PhotoSize = update.message.photo[-1]
    bytearray: bytes = photo.get_file().download_as_bytearray()
    img = Image.open(io.BytesIO(bytearray))
    update.message.reply_text(predict[context.bot_data[user_id]](img))


def document_image_handler(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    
    if user_id not in context.bot_data:
        update.message.reply_text('You have to select the classifier using the /classifier command.')
        return

    document: Document = update.message.document
    bytearray: bytes = document.get_file().download_as_bytearray()
    img = Image.open(io.BytesIO(bytearray))
    update.message.reply_text(predict[context.bot_data[user_id]](img))


def default(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('I don\'t really know how to respond to that. I think you should try the /help command.')


def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to Doctor CVC.')
    update.message.reply_text('To select one of our computer vision models you have to use the /classifier command')
    update.message.reply_text('After selecting the classifier you want to use, send a photo and you will receive an ansewr almost immediately')
    update.message.reply_text('To change the classifier use the /classifier command again.')


def main(token) -> None:
    updater = Updater(token)

    updater.dispatcher.add_handler(CommandHandler([ 'start', 'help' ], help))
    updater.dispatcher.add_handler(CommandHandler('classifier', select_classifier_handler))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
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
