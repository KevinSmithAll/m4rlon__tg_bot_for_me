from bot_system import bot, check_admin
import functions

@bot.message_handler(commands=['prognoz'])
@check_admin
def forecast(message):
    bot.send_message(message.chat.id, functions.forecaster())