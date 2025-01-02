import schedule
import threading
import time
from bot_system import bot, loop


def start_polling():
    bot.polling(none_stop=True)


#polling_thread = threading.Thread(target=start_polling)
#polling_thread.start()

#schedule.every().day.at("09:10").do(loop)

def main():
    polling_thread = threading.Thread(target=start_polling)
    polling_thread.start()

    schedule.every().day.at("09:10").do(loop)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()