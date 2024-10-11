from telebot.types import  ReplyKeyboardMarkup, KeyboardButton


def buttons():

    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(KeyboardButton("Video"), KeyboardButton("Audio"))

    return markup

