from bot_system import bot, check_admin
import functions
from telebot import types
from database import Database



@bot.message_handler(commands=['remind'])
@check_admin
def remember(message):
    markup_new = types.InlineKeyboardMarkup(row_width=1)
    item_1 = types.InlineKeyboardButton('Добавить заметку', callback_data='Add_zametka')
    item_2 = types.InlineKeyboardButton('Редактировать заметку', callback_data='Redact')
    item_3 = types.InlineKeyboardButton('Удалить заметку', callback_data='Del')
    item_4 = types.InlineKeyboardButton('Просмотреть все заметки', callback_data='Check_all')
    markup_new.add(item_1, item_2, item_3, item_4)
    bot.send_message(message.chat.id, 'Что будем делать?', reply_markup=markup_new)

remind_cmds = ['Add_zametka', 'Redact', 'Del', 'Check_all']
@bot.callback_query_handler(func=lambda call: call.data in remind_cmds)
def call_back2(call):
    if call.data == 'Add_zametka':
        bot.send_message(call.message.chat.id, 'Введите Вашу заметку')
        bot.register_next_step_handler(call.message, add_zametka)
    elif call.data == 'Redact':
        print('Test')
    elif call.data == 'Del':
        pass
    elif call.data == 'Check_all':
        pass


def add_zametka(message):
    db = Database()
    db.add_text(message.text)
    db.__del__()
    bot.reply_to(message, 'Ваша заметка добавлено успешно')