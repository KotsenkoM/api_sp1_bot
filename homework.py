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
url = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'
headers = {'Authorization': f'OAuth {PRAKTIKUM_TOKEN}'}


def parse_homework_status(homework):
    homework_name = homework['homework_name']
    status = homework['status']
    if status != 'approved':
        verdict = 'К сожалению, в работе нашлись ошибки.'
    else:
        verdict = 'Ревьюеру всё понравилось, работа зачтена!'
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homeworks(current_timestamp):
    payload = {'from_date': current_timestamp}
    homework_statuses = requests.get(url, headers=headers, params=payload)
    return homework_statuses.json()


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
            homework = homeworks['homeworks'][0]
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
