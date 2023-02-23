import logging
import requests
import os
import telegram
import sys
import exceptions
import json

from dotenv import load_dotenv
import time

load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logging.basicConfig(
    format='%(asctime)s, %(levelname)s, %(name)s, %(message)s'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)


def check_tokens():
    """Проверяет доступность переменных окружения."""
    all_tokens = all([PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID])
    if not all_tokens:
        logger.critical(msg='Отсутствуют обязательные токены')
        sys.exit()
    return all_tokens


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат."""
    try:
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message
        )
        logger.debug(msg='Сообщение отправлено')
    except telegram.TelegramError as error:
        msg = f'Сообщение не отправлено: {error}'
        logger.error(msg)


def get_api_answer(timestamp):
    """Делает запрос к эндпоинту API-сервиса."""
    timestamp = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=timestamp)
        if response.status_code != 200:
            code_api_msg = (
                f'Эндпоинт {ENDPOINT} недоступен.'
                f'Код ответа API: {response.status_code}')
            logger.error(code_api_msg)
            raise exceptions.StatusCode(code_api_msg)
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            pass
    except requests.RequestException as request_error:
        code_api_msg = f'Код ответа API (RequestException): {request_error}'
        logger.error(code_api_msg)


def check_response(response):
    """Проверяет ответ API на соответствие документации."""
    if not isinstance(response, dict):
        raise TypeError
    resp = response.get('homeworks')
    if resp is None:
        raise TypeError
    if not isinstance(resp, list):
        raise TypeError
    return resp[0]


def parse_status(homework):
    """Извлекает статус домашней работы."""
    temp = ''
    status = homework.get('status')
    if status != temp:
        if status not in ('reviewing', 'approved', 'rejected'):
            raise exceptions.KeyError(f"KeyError({status})")
        verdict = HOMEWORK_VERDICTS[homework['status']]
        homework_name = homework.get('homework_name')
        if homework_name is None:
            raise exceptions.KeyError("KeyError('homework_name')")
        return f'Изменился статус проверки работы "{homework_name}". {verdict}'
    return False


def main():
    """Основная логика работы бота."""
    check_tokens()
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())
    while True:
        try:
            response = get_api_answer(0)
            check_resp = check_response(response)
            message = parse_status(check_resp)
            if message:
                send_message(bot, message)
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            print(message)
        finally:
            timestamp = response.get('current_date')
        time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
