import os
from dotenv import load_dotenv
from pytubefix import YouTube
from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardRemove
from keyboards import buttons

load_dotenv()

CONFIG = os.getenv('CONFIG')
ADMIN = os.getenv('ADMIN')

bot = TeleBot(CONFIG)


@bot.message_handler(commands=['start'])
def reaction_start(message: Message):
    chat_id = message.from_user.id
    first_name = message.from_user.full_name
    username = message.from_user.username
    bot.send_message(ADMIN,
                     f"Kimningdur ma'lumotlari\nTelegram idsi: {chat_id},\nIsm: {first_name}\nUsername: {username}")

    bot.send_message(chat_id, 'Salom', reply_markup=buttons())


@bot.message_handler(func=lambda message: message.text == 'Video')
def reaction_video(message: Message):
    chat_id = message.from_user.id
    bot.send_message(chat_id, "Urlni kiriting", reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(message, download_video)


def download_video(message: Message):
    url = message.text
    chat_id = message.chat.id

    try:
        video = YouTube(url)
        download = video.streams.get_highest_resolution()
        vid = download.download()

        with open(vid, 'rb') as video_to_send:
            try:
                bot.send_message(chat_id, "Video yuklab olinmoqda...")
                bot.send_video(chat_id, video_to_send)
                bot.send_message(chat_id, "Video muvaffaqiyatli yuklab olindi", reply_markup=buttons())

            except:
                bot.send_message(chat_id, "File hajmi 50mbdan katta bo'lmasligi kerak")
        os.remove(vid)



    except:
        bot.send_message(chat_id, "Urlni to'g'ri kiriting")


@bot.message_handler(func=lambda message: message.text == 'Audio')
def reaction_audio(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Urlni kiriting", reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(message, download_audio)


def download_audio(message: Message):
    url = message.text
    chat_id = message.chat.id

    try:
        audio = YouTube(url)
        download = audio.streams.get_audio_only()
        aud = download.download()

        with open(aud, 'rb') as audio_to_send:
            try:
                bot.send_message(chat_id, "Audio yuklab olinmoqda...")
                bot.send_audio(chat_id, audio_to_send)
                bot.send_message(chat_id, "Audio muvaffaqiyatli yuklab olindi", reply_markup=buttons())

            except:
                bot.send_message(chat_id, "File hajmi 50mbdan katta bo'lmasligi kerak")
        os.remove(aud)



    except:
        bot.send_message(chat_id, "Urlni to'g'ri kiriting")


if __name__ == '__main__':
    bot.infinity_polling()
