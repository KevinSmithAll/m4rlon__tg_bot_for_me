from bot_system import bot, check_admin
from databases.users import User_db

@bot.message_handler(commands=['start'])
@check_admin
def main(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    db = User_db()
    
    if db.user_exists(tg_id=user_id) == False:
        msg = f'Привет, добро пожаловать, я тебя внёс в базу. Я полностью к твоим услугам'
        bot.send_message(chat_id, text=msg)
    else:
        msg = f'Привет, ты уже прошел регистрацию'
        bot.send_message(chat_id, text=msg)