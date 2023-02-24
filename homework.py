import json
import logging
import os
import sys
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv

import exceptions

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


format = logging.Formatter('%(asctime)s, %(levelname)s, %(name)s, %(message)s')


logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(format)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)


def check_tokens():
    """Проверяет доступность переменных окружения."""
    logger.debug('Проверяю токены.')
    tokens = ('PRACTICUM_TOKEN', 'TELEGRAM_TOKEN', 'TELEGRAM_CHAT_ID')
    missing_tokens = [token for token in tokens if globals()[token] is None]
    if missing_tokens:
        logger.critical(f'Программа останолена. Нет токена: {missing_tokens}')
        sys.exit()
    logger.debug('Все токены а месте.')


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат."""
    logger.debug('Попытался отправить сообщение.')
    try:
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message
        )
    except telegram.TelegramError as error:
        msg = f'Сообщение не отправлено: {error}'
        logger.error(msg)
    logger.debug(msg='Сообщение отправлено')


def get_api_answer(timestamp):
    """Делает запрос к эндпоинту API-сервиса."""
    logger.debug('Отправлен запрос к API.')
    params = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
    except requests.RequestException as request_error:
        code_api_msg = f'Ошибка при отправке запроса к API: {request_error}'
        raise ConnectionError(code_api_msg)
    logger.debug('Запрос успешный. Ответ получен.')
    if response.status_code != HTTPStatus.OK:
        code_api_msg = (
            f'Эндпоинт {ENDPOINT} недоступен.'
            f'Код ответа API: {response.status_code}')
        raise exceptions.StatusCode(code_api_msg)
    try:
        return response.json()
    except json.decoder.JSONDecodeError:
        raise json.decoder.JSONDecodeError(
            'Ошибка с приведением к нужному типу данных'
        )


def check_response(response):
    """Проверяет ответ API на соответствие документации."""
    logger.debug('Началасть проверка полученного ответа.')
    if not isinstance(response, dict):
        raise TypeError('Ошибка типа данных')
    resp = response.get('homeworks')
    if resp is None:
        raise TypeError('Ошибка типа данных')
    if not isinstance(resp, list):
        raise TypeError('Ошибка типа данных')
    return resp


def parse_status(homework):
    """Извлекает статус домашней работы."""
    logger.debug('Началасть проверка статуса домашней работы.')
    if 'homework_name' not in homework.keys():
        raise KeyError("KeyError('homework_name')")
    homework_name = homework.get('homework_name')
    status = homework.get('status')
    if status not in HOMEWORK_VERDICTS.keys():
        raise KeyError(f"KeyError({status})")
    verdict = HOMEWORK_VERDICTS[homework['status']]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""
    check_tokens()
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())
    tmp_status = 'reviewing'
    while True:
        try:
            response = get_api_answer(timestamp)
            check_resp = check_response(response)
            if len(check_resp) == 0:
                msg = 'На проверке нет домашних работ'
                logger.debug(msg)
                send_message(bot, msg)
                continue
            else:
                check_resp = check_resp[0]
            status = check_resp['status']
            if status != tmp_status:
                msg = 'Изменений нет, ждем 10 минут и проверяем API'
                logger.debug(msg)
                send_message(bot, msg)
            message = parse_status(check_resp)
            timestamp = response.get('current_date')
            tmp_status = status
            send_message(bot, message)
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.critical(message)
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
