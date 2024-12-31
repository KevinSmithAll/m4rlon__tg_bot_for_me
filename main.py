import schedule
import threading
import time
from bot_system import bot, loop, happy_new_year


def start_polling():
    bot.polling(none_stop=True)


#polling_thread = threading.Thread(target=start_polling)
#polling_thread.start()

#schedule.every().day.at("09:10").do(loop)

def main():
    polling_thread = threading.Thread(target=start_polling)
    polling_thread.start()

    schedule.every().day.at("09:10").do(loop)
    schedule.every().day.at("00:01").do(happy_new_year)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()