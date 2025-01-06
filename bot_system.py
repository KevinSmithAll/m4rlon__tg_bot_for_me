import telebot
from config import *
import functions
import sys



bot = telebot.TeleBot(TOKEN)

def loop():
    bot.send_message(890424948, functions.weaher_9pm())


def check_admin(func):
    def wrapper(message, *args, **kwargs):
        if message.from_user.id != LOGIN_ID:
            bot.reply_to(message, text='Извини, дружище (подружище), но этот Бот работает только на 1 человека. Если интересно заходи на мой Git Verse.')
        else: return func(message, *args, **kwargs)
    return wrapper

from bot_functions.finance_func import *
from bot_functions.prognoz_func import *
from bot_functions.remind_func import *
from bot_functions.start_func import *