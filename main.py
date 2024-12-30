import telebot
from telebot import types
import functions
from database import Database
import matplotlib.pyplot as plt
import matplotlib
import schedule
import threading
import time

from config import LOGIN_ID, TOKEN, LIMITS, CATEGORIES

bot = telebot.TeleBot(TOKEN)


"""
def private_access():
    def deco_restrict(f):

        @wraps(f)
        def f_restrict(message, *args, **kwargs):
            username = message.from_user.id

            if message.from_user.id == LOGIN_ID:
                return f(message, *args, **kwargs)
            else:
                bot.reply_to(message, text='Пошел нахуй, пошел нахуй, пошел нахуй... ПИДОРАС')

        return f_restrict  # true decorator

    return deco_restrict
"""

def check_admin(func):
    def wrapper(message, *args, **kwargs):
        if message.from_user.id != LOGIN_ID:
            bot.reply_to(message, text='Пошел нахуй, пошел нахуй, пошел нахуй... ПИДОРАС')
        else: return func(message, *args, **kwargs)
    return wrapper

@bot.message_handler(commands=['start'])
#@private_access()
@check_admin
def main(message):
    bot.send_message(message.from_user.id, 'Привет, Кирилл, я твой помощник')
    bot.send_message(message.chat.id, f'Вот твой ИД {message.from_user.id}')
    #bot.send_message(message.chat.id, f'Вот ИД чата {message.from_user.id}')

@bot.message_handler(commands=['prognoz'])
@check_admin
def forecast(message):
    bot.send_message(message.chat.id, functions.forecaster())

def add_zametka(message):
    db = Database()
    db.add_text(message.text)
    db.__del__()
    bot.reply_to(message, 'Ваша заметка добавлено успешно')



def loop():
    bot.send_message(890424948, functions.forecaster())

@bot.message_handler(commands=['finance'])
@check_admin
def finance(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item_1 = types.InlineKeyboardButton('Добавить расход', callback_data='Add')
    item_2 = types.InlineKeyboardButton('Просмотреть расходы за 7 дней', callback_data='Check_7')
    item_3 = types.InlineKeyboardButton('Прислать отчёт за весь период', callback_data='Check_all')
    item_4 = types.InlineKeyboardButton('Удалить какой-то расход за последние 7 дней', callback_data='Delete_some')
    item_5 = types.InlineKeyboardButton('Изменить какой-то расход за последние 7 дней', callback_data='change_rashod')
    item_6 = types.InlineKeyboardButton('Просмотреть остатки', callback_data='check')
    item_7 = types.InlineKeyboardButton('Показать диаграмму расходов', callback_data='show_diagram')
    item_8 = types.InlineKeyboardButton('Начать новый месяц', callback_data='restart_month')
    markup.add(item_1, item_2, item_3, item_4, item_5, item_6, item_7, item_8)
    bot.send_message(message.chat.id, 'Что будем делать?', reply_markup=markup)

finance_cmds = ['Add', 'Check_7', 'Check_all', 'Delete_some', 'change_rashod', 'check', 'show_diagram', 'restart_month']
@bot.callback_query_handler(func=lambda call: call.data in finance_cmds)
def call_back(call):
    if call.data == 'Add':
        bot.send_message(call.message.chat.id, 'Введите ваш расход по следующей форме: *дата* *сумма* *категория* *примечание*')
        bot.register_next_step_handler(call.message, add_rashod)
    elif call.data == 'Check_7':
        db = Database()
        list_ = db.get_7_day()
        for row in list_:
            bot.send_message(call.message.chat.id, text=f'№ п/п: <b>{str(row[0])}</b>\n'
                                                        f'Сумма: <b>{str(row[1])}</b>\n'
                                                        f'Дата: <b>{str(row[2])}</b>\n'
                                                        f'Категория: <b>{str(row[3])}</b>\n'
                                                        f'Примечание: <b>{str(row[4])}</b>', parse_mode='HTML')
        db.__del__()
    elif call.data == 'Check_all':
        db = Database()
        db.export()
        with open('export.xlsx', 'rb') as f:
            bot.send_document(call.message.chat.id, f)
        db.__del__()
    elif call.data == 'Delete_some':
        db = Database()
        for row in db.get_7_day():
            bot.send_message(call.message.chat.id, text=f'Номер расхода: <b>{str(row[0])}</b>\n'
                                                        f'Сумма: <b>{str(row[1])}</b>\n'
                                                        f'Дата: <b>{str(row[2])}</b>\n'
                                                        f'Категория: <b>{str(row[3])}</b>\n'
                                                        f'Примечание: <b>{str(row[4])}</b>', parse_mode='HTML')
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
                                                        f'Примечание: <b>{str(row[4])}</b>', parse_mode='HTML')
        bot.send_message(call.message.chat.id, text='Введите измененный расход в формате:\n'
                                                    '*№* *дата* *сумма* *категория* *комментарий*')
        bot.register_next_step_handler(call.message, change_rashod)
        db.__del__()
    elif call.data == 'check':
        limit_list = []
        db = Database()
        for kategor in CATEGORIES:
            sum = db.get_sum(kategor)
            if sum != None:
                limit_list.append(sum)
            else:
                limit_list.append(0)
        ostatok = [x - y for x, y in zip(LIMITS, limit_list)]
        bot.send_message(call.message.chat.id, text=f'Текущий остаток по каждой категории:\n'
                                                    f'ЕДА: <b>{str(ostatok[0])} руб</b>\n'
                                                    f'ПРОЕЗД: <b>{str(ostatok[1])} руб</b>\n'
                                                    f'ГИГИЕНА: <b>{str(ostatok[2])} руб</b>\n'
                                                    f'ЛИЧНОЕ: <b>{str(ostatok[3])} руб</b>', parse_mode='HTML')
        db.__del__()
    elif call.data == 'show_diagram':
        limit_list = []
        db = Database()
        for kategor in CATEGORIES:
            sum = db.get_sum(kategor)
            if sum != None:
                limit_list.append(sum)
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
        with open('itog.xlsx', 'rb') as f:
            bot.send_document(call.message.chat.id, f)
        db.delete_month()
        db.__del__()

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
    db = Database()
    if db.is_id(int(message.text)):
        db.delete_row(int(message.text))
        bot.reply_to(message, f'Расход №{message.text} удален')
        db.__del__()
    else:
        bot.send_message(message.chat.id, 'Расхода с таким ИД не существует')
        bot.register_next_step_handler(message, delete_rashod)

def add_rashod(message):
    print(functions.correct_variant(' '.join(message.text.split()[0:3])))
    if functions.correct_variant(' '.join(message.text.split()[0:3])):
        data_list = message.text.split()
        db = Database()
        if len(data_list)== 4: db.insert(data_list[1], data_list[0], data_list[2], data_list[3])
        else: db.insert(sum=data_list[1], date=data_list[0], kategor=data_list[2])
        db.__del__()
        bot.reply_to(message, 'Расход успешно добавлен')
    else:
        bot.send_message(message.chat.id, 'Ошибка ввода')
        bot.register_next_step_handler(message, add_rashod)



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

    #db = Database()
    #db.add_text(message.text)
    #bot.reply_to(message, text='Заметка добавлена я моё хранилище')
    #db.__del__()


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



def start_polling():
    bot.polling(none_stop=True)


polling_thread = threading.Thread(target=start_polling)
polling_thread.start()

schedule.every().day.at("09:10").do(loop)

while True:
    schedule.run_pending()
    time.sleep(1)