import os
import time
import requests
import telegram
import logging
from dotenv import load_dotenv


load_dotenv()

PRAKTIKUM_TOKEN = os.getenv('PRAKTIKUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

bot = telegram.Bot(token=TELEGRAM_TOKEN)
URL = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRAKTIKUM_TOKEN}'}


def parse_homework_status(homework):
    homework_name = homework.get('homework_name')
    status = homework.get('status')
    if status is None or homework_name is None:
        return logging.error('Неверный ответ сервера')
    if status != 'approved':
        verdict = 'К сожалению, в работе нашлись ошибки.'
    else:
        verdict = 'Ревьюеру всё понравилось, работа зачтена!'
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homeworks(current_timestamp=int(time.time())):
    payload = {'from_date': current_timestamp}
    try:
        homework_statuses = requests.get(URL, headers=HEADERS, params=payload)
        return homework_statuses.json()
    except Exception as error:
        logging.exception(f'Бот упал с ошибкой: {error}')
        send_message(text=logging.exception)
        return {}


def send_message(message):
    return bot.send_message(CHAT_ID, message)


def main():
    logging.info('Бот запущен')
    logging.debug('api_sp1_bot')
    current_timestamp = int(time.time())

    while True:
        try:
            homeworks = get_homeworks(current_timestamp)
            if len(homeworks.get('homeworks')) == 0:
                time.sleep(20 * 60)
                continue
            homework = homeworks.get('homeworks')[0]
            message = parse_homework_status(homework)
            send_message(message)
            time.sleep(20 * 60)

        except Exception as e:
            send_message(f'Бот упал с ошибкой: {e}')
            time.sleep(5)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        filename='api_sp1_bot.log',
        format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
    )
    main()
