# API Telegraam Bot

Через определенное количество времени бот отправляет запрос к API Яндекс для проверки статуса домашней работы.
Если статус изменился, бот присылает сообщение.

## Особенности

- Все токены хранятся локально '.env'
- Логгирование в консоли
- Если произошла ошибка в работе бота, будет отправлено сообщение


## Установка

Клонировать репозиторий
```sh
git@github.com:aleksandrkomyagin/homework_bot.git
```
Создать вирутальное окружение
```sh
cd homework_bot/
```
```sh
python -m venv venv
```
Активировать его
```sh
source venv/Scripts/activate
```
Установить зависимости
```sh
pip install -r requirements.txt
```
Создать файл .env
```sh
touch .env
```
Добавить информацию в файл .env
```sh
PRACTICUM_TOKEN = Ваш токен
TELEGRAM_TOKEN = Ваш телеграм токен 
TELEGRAM_CHAT_ID = Ваш ID телеграм бота
```
Запустить бота
```sh
python homework.py
```

Как получить ID телеграм бота:
1. Найти бота https://t.me/userinfobot;
2. Отправить команду /start;