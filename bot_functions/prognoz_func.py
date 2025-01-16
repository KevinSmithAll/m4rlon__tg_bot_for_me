from bot_system import bot, check_admin
import functions
from telebot import types


@bot.message_handler(commands=['prognoz'])
@check_admin
def remember(message):
    markup_new = types.InlineKeyboardMarkup(row_width=1)
    item_1 = types.InlineKeyboardButton('Погода сейчас', callback_data='Weather_now')
    item_2 = types.InlineKeyboardButton('Погода на завтра', callback_data='Weather_tomorrow')
    item_3 = types.InlineKeyboardButton('Погода на завтра УТРО', callback_data='Weather_morning')
    item_4 = types.InlineKeyboardButton('Погода в течение недели', callback_data='Weather_week')
    markup_new.add(item_1, item_2, item_3, item_4)
    bot.send_message(message.chat.id, 'Что будем делать?', reply_markup=markup_new)

weather_cmds = ['Weather_now', 'Weather_tomorrow', 'Weather_morning', 'Weather_week']
#bot.register_next_step_handler(call.message, change_rashod)
@bot.callback_query_handler(func=lambda call: call.data in weather_cmds)
def call_back2(call):
    if call.data == 'Weather_now':
        bot.send_message(call.message.chat.id, functions.forecaster())
    elif call.data == 'Weather_tomorrow':
        index_ = functions.get_tomorrow_index()
        bot.send_message(call.message.chat.id, functions.weather_tomorrow(index=index_))
    elif call.data == 'Weather_morning':
        index_ = functions.get_morning_index()
        bot.send_message(call.message.chat.id, functions.weather_tomorrow(index=index_))
    elif call.data == 'Weather_week':
        dates = functions.get_week_dates()
        
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton(dates[1])
        btn2 = types.KeyboardButton(dates[2])
        btn3 = types.KeyboardButton(dates[3])
        btn4 = types.KeyboardButton(dates[4])
        btn5 = types.KeyboardButton('Назад')
        markup.row(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(call.message.chat.id, text='На какой день Вы хотите узнать прогноз?', reply_markup=markup)
        bot.register_next_step_handler(call.message, get_weather)


def get_weather(message) -> None:
    dates = functions.get_week_dates()
    indexes = functions.get_4_day_index()

    if message.text == str(dates[1]):
        bot.send_message(message.chat.id, functions.weather_tomorrow(index=indexes[dates[1]]))
        bot.register_next_step_handler(message, get_weather)
    elif message.text == str(dates[2]):
        bot.send_message(message.chat.id, functions.weather_tomorrow(index=indexes[dates[2]]))
        bot.register_next_step_handler(message, get_weather)
    elif message.text == str(dates[3]):
        bot.send_message(message.chat.id, functions.weather_tomorrow(index=indexes[dates[3]]))
        bot.register_next_step_handler(message, get_weather)
    elif message.text == str(dates[4]):
        bot.send_message(message.chat.id, functions.weather_tomorrow(index=indexes[dates[4]]))
        bot.register_next_step_handler(message, get_weather)
    elif message.text == 'Назад':
        deleted_ = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Возвращение назад', reply_markup=deleted_)
    else:
        bot.send_message(message.chat.id, 'Неверный ввод')
        