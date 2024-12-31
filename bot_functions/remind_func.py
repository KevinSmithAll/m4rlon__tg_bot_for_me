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
    item_4 = types.InlineKeyboardButton('Удалить все заметки', callback_data='Delete_all')
    item_5 = types.InlineKeyboardButton('Просмотреть все заметки', callback_data='Show_all')
    markup_new.add(item_1, item_2, item_3, item_4, item_5)
    bot.send_message(message.chat.id, 'Что будем делать?', reply_markup=markup_new)

remind_cmds = ['Add_zametka', 'Redact', 'Del', 'Show_all', 'Delete_all']
@bot.callback_query_handler(func=lambda call: call.data in remind_cmds)
def call_back2(call):
    if call.data == 'Add_zametka':
        bot.send_message(call.message.chat.id, 'Введите Вашу заметку')
        bot.register_next_step_handler(call.message, add_zametka)
    elif call.data == 'Redact':
        db = Database()
        for row in db.get_all_text():
            bot.send_message(call.message.chat.id, text=f'№ п/п: {row[0]}\n'
                                                        f'Заметка: {row[1]}')
        bot.send_message(call.message.chat.id, 'Введите измененную заметку в виде: *№* *Заметка*')
        bot.register_next_step_handler(call.message, edit_zametka)
        db.__del__()
    elif call.data == 'Show_all':
        db = Database()
        for row in db.get_all_text():
            bot.send_message(call.message.chat.id, text=f'№ п/п: {row[0]}\n'
                                                        f'Заметка: {row[1]}')
        db.__del__()
    elif call.data == 'Del':
        db = Database()
        for row in db.get_all_text():
            bot.send_message(call.message.chat.id, text=f'№ п/п: {row[0]}\n'
                                                        f'Заметка: {row[1]}')
        bot.send_message(call.message.chat.id, 'Введите номер удаляемой заметки')
        bot.register_next_step_handler(call.message, del_zametka)
        db.__del__()
    elif call.data == 'Delete_all':
        db = Database()
        db.delete_all_zametka()
        bot.send_message(call.message.chat.id, 'Все заметки удалены успешно')
        db.__del__()

def del_zametka(message):
    db = Database()
    db.delete_zametka(message.text)
    bot.send_message(message.chat.id, 'Заметка успешно удалена')
    db.__del__()

def edit_zametka(message):
    db = Database()
    if functions.correct_zametka(message.text):
        db.change_text(message.text.split()[0], message.text.split()[1])
        bot.reply_to(message, 'Ваша заметка изменена успешно')
    else:
        bot.reply_to(message, 'Неверный формат')
        bot.register_next_step_handler(message, add_zametka)


def add_zametka(message):
    db = Database()
    db.add_text(message.text)
    db.__del__()
    bot.reply_to(message, 'Ваша заметка добавлено успешно')