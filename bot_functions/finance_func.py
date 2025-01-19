from bot_system import bot
from telebot import types
from bot_system import check_admin
from database import Database
from config import *
import matplotlib.pyplot as plt
import matplotlib
import functions
from databases.transactions import Transaction_db

@bot.message_handler(commands=['finance'])
@check_admin
def finance(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item_1 = types.InlineKeyboardButton('Добавить расход', callback_data='Add')
    item_2 = types.InlineKeyboardButton('Просмотреть расходы за 7 дней', callback_data='Check_7')
    item_2_1 = types.InlineKeyboardButton('Просмотреть расходы за 3 дня', callback_data='Check_3')
    item_3 = types.InlineKeyboardButton('Прислать отчёт за весь период', callback_data='Check_all')
    item_4 = types.InlineKeyboardButton('Удалить какой-то расход за последние 7 дней', callback_data='Delete_some')
    item_5 = types.InlineKeyboardButton('Изменить какой-то расход за последние 7 дней', callback_data='change_rashod')
    item_6 = types.InlineKeyboardButton('Просмотреть остатки', callback_data='check')
    item_7 = types.InlineKeyboardButton('Показать диаграмму расходов', callback_data='show_diagram')
    item_8 = types.InlineKeyboardButton('Начать новый месяц', callback_data='restart_month')
    markup.add(item_1, item_2, item_2_1, item_3, item_4, item_5, item_6, item_7, item_8)
    bot.send_message(message.chat.id, 'Что будем делать?', reply_markup=markup)

finance_cmds = ['Add', 'Check_7', 'Check_3', 'Check_all', 'Delete_some', 'change_rashod', 'check', 'show_diagram', 'restart_month']
@bot.callback_query_handler(func=lambda call: call.data in finance_cmds)
def call_back(call):
    user_id = call.message.chat.id
    if call.data == 'Add':
        bot.send_message(call.message.chat.id, 'Введите ваш расход по следующей форме: *дата* *сумма* *категория* *примечание*')
        bot.register_next_step_handler(call.message, add_rashod)
    elif call.data == 'Check_7':
        db = Transaction_db()
        list_ = db.get_7_day(tg_id=user_id)
        for number, row in enumerate(list_):
            bot.send_message(call.message.chat.id, text=f'№ п/п: <b>{number + 1}</b>\n'
                                                        f'Сумма: <b>{str(row[0])}</b>\n'
                                                        f'Дата: <b>{str(row[1])}</b>\n'
                                                        f'Категория: <b>{str(row[2])}</b>\n'
                                                        f'Комментарий: <b>{str(row[3])}</b>', parse_mode='HTML')
        db.__del__()
    elif call.data == 'Check_3':
        db = Transaction_db()
        list_ = db.get_3_day(tg_id=user_id)
        for number, row in enumerate(list_):
            bot.send_message(call.message.chat.id, text=f'№ п/п: <b>{number + 1}</b>\n'
                                                        f'Сумма: <b>{str(row[0])}</b>\n'
                                                        f'Дата: <b>{str(row[1])}</b>\n'
                                                        f'Категория: <b>{str(row[2])}</b>\n'
                                                        f'Комментарий: <b>{str(row[3])}</b>', parse_mode='HTML')
    elif call.data == 'Check_all':
        db = Transaction_db()
        db.export_transactions(tg_id=user_id)
        with open('export.xlsx', 'rb') as f:
            bot.send_document(call.message.chat.id, f)
        db.__del__()
    elif call.data == 'Delete_some':
        db = Transaction_db()
        list_ = db.get_7_day(tg_id=user_id)
        for number, row in enumerate(list_):
            bot.send_message(call.message.chat.id, text=f'№ п/п: <b>{number + 1}</b>\n'
                                                        f'Сумма: <b>{str(row[0])}</b>\n'
                                                        f'Дата: <b>{str(row[1])}</b>\n'
                                                        f'Категория: <b>{str(row[2])}</b>\n'
                                                        f'Комментарий: <b>{str(row[3])}</b>', parse_mode='HTML')
        bot.send_message(call.message.chat.id, text='Введите номер удаляемого расхода')
        bot.register_next_step_handler(call.message, delete_rashod)
        db.__del__()
    elif call.data == 'change_rashod':
        db = Database()
        for row in db.get_7_day():
            bot.send_message(call.message.chat.id, text=f'Номер расхода: <b>{str(row[0])}</b>\n'
                                                        f'Сумма: <b>{str(row[1])}</b>\n'
                                                        f'Дата: <b>{str(row[2])}</b>\n'
                                                        f'Категория: <b>{str(row[3])}</b>\n'
                                                        f'Комментарий: <b>{str(row[4])}</b>', parse_mode='HTML')
        bot.send_message(call.message.chat.id, text='Введите измененный расход в формате:\n'
                                                    '*№* *дата* *сумма* *категория* *комментарий*')
        bot.register_next_step_handler(call.message, change_rashod)
        db.__del__()
    elif call.data == 'check':
        limit_list = []
        db = Database()
        for kategor in CATEGORIES:
            suma = db.get_sum(kategor)
            if suma != None:
                limit_list.append(suma)
            else:
                limit_list.append(0)
        ostatok = [x - y for x, y in zip(LIMITS, limit_list)]
        bot.send_message(call.message.chat.id, text=f'Текущий остаток по каждой категории:\n'
                                                    f'ЕДА: <b>{str(ostatok[0])} руб</b>\n'
                                                    f'ПРОЕЗД: <b>{str(ostatok[1])} руб</b>\n'
                                                    f'ГИГИЕНА: <b>{str(ostatok[2])} руб</b>\n'
                                                    f'ЛИЧНОЕ: <b>{str(ostatok[3])} руб</b>\n'
                                                    f'СУММАРНЫЙ ОСТАТОК: <b>{str(sum(ostatok))}</b>', parse_mode='HTML')
        db.__del__()
    elif call.data == 'show_diagram':
        limit_list = []
        db = Database()
        for kategor in CATEGORIES:
            suma = db.get_sum(kategor)
            if suma != None:
                limit_list.append(suma)
            else:
                limit_list.append(0)
        ostatok = [x - y for x, y in zip(LIMITS, limit_list)]
        matplotlib.use('agg')
        plt.bar(CATEGORIES, LIMITS, label='Выделено')
        plt.bar(CATEGORIES, ostatok, label='Осталось')
        plt.legend(loc='best')
        plt.grid()
        plt.savefig('diagram.png')
        ph = open('diagram.png', 'rb')
        bot.send_message(call.message.chat.id, 'Диаграмма расходов:')
        bot.send_photo(call.message.chat.id, ph)
        plt.clf()
        ph.close()
        db.__del__()
    elif call.data == 'restart_month':
        bot.send_message(call.message.chat.id, text='Высылаю отчёт за весь месяц перед удалением')
        db = Database()
        db.export()
        with open('export.xlsx', 'rb') as f:
            bot.send_document(call.message.chat.id, f)
        db.delete_month()
        db.__del__()
    bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  reply_markup=None)  

def change_rashod(message):
    if functions.correct_with_number(' '.join(message.text.split()[0:4])):
        data_list = message.text.split()
        db = Database()
        if len(data_list)== 5: db.change(data_list[0], data_list[2], data_list[1], data_list[3], data_list[4])
        else: db.change(data_list[0], data_list[2], data_list[1], data_list[3])
        db.__del__()
        bot.reply_to(message, 'Расход успешно изменен')
    else:
        bot.send_message(message.chat.id, 'Ошибка ввода')
        bot.register_next_step_handler(message, change_rashod)

def delete_rashod(message):
    user_id = message.from_user.id
    db = Transaction_db()
    
    count = db.get_7_day(tg_id=user_id)
    
    try:
        if int(message.text) > count:
            raise ValueError
        else:
            transaction_id = 
    except ValueError:
        bot.send_message(message.chat.id, 'Ошибка ввода')
    
    
    
    
    
    if db.is_id(int(message.text)):
        db.delete_row(int(message.text))
        bot.reply_to(message, f'Расход №{message.text} удален')
        db.__del__()
    else:
        bot.send_message(message.chat.id, 'Расхода с таким ИД не существует')
        bot.register_next_step_handler(message, delete_rashod)

def add_rashod(message):
    user_id = message.from_user.id
    
    if functions.correct_variant(' '.join(message.text.split()[0:3])):
        data_list = message.text.split()
        db = Transaction_db()
        if len(data_list) == 3:
            db.add_transaction(tg_id=user_id,
                               date=data_list[0],
                               value=data_list[1],
                               category=data_list[2])
        else: 
            db.add_transaction(tg_id=user_id,
                               date=data_list[0],
                               value=data_list[1],
                               category=data_list[2],
                               comment=' '.join(data_list[3:]))
        db.__del__()
        bot.reply_to(message, 'Расход успешно добавлен')
    else:
        bot.send_message(message.chat.id, 'Ошибка ввода, вероятно нарушен шаблон, попробуйте ещё раз')
        bot.register_next_step_handler(message, add_rashod)
