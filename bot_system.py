import telebot
from config import *
import functions
import sys



bot = telebot.TeleBot(TOKEN)

def loop():
    bot.send_message(890424948, functions.forecaster())


def check_admin(func):
    def wrapper(message, *args, **kwargs):
        if message.from_user.id != LOGIN_ID:
            bot.reply_to(message, text='Пошел нахуй, пошел нахуй, пошел нахуй... ПИДОРАС')
        else: return func(message, *args, **kwargs)
    return wrapper

sys.path.append('bot_functions')
import finance_func, start_func, prognoz_func, remind_func