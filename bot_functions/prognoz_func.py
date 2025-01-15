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

@bot.callback_query_handler(func=lambda call: call.data in weather_cmds)
def call_back2(call):
    if call.data == 'Weather_now':
        bot.send_message(call.message.chat.id, functions.forecaster())
    elif call.data == 'Redact':
        pass