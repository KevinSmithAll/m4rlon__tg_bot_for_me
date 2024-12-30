from bot_system import bot, check_admin


@bot.message_handler(commands=['start'])
@check_admin
def main(message):
    bot.send_message(message.from_user.id, 'Привет, Кирилл, я твой помощник')
    bot.send_message(message.chat.id, f'Вот твой ИД {message.from_user.id}')
    #bot.send_message(message.chat.id, f'Вот ИД чата {message.from_user.id}')