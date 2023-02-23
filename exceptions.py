import telegram
from requests.exceptions import RequestException


class IndexError(Exception):
    """Ошибка при извлечении элемента по индексу."""

    def __init__(self, *args):
        """Переопределение нужного поля."""
        self.IndexError = 'На проверке нет работ'

    def __str__(self):
        """Отображение в нужном формате."""
        return self.IndexError


class KeyError(Exception):
    """Ошибка при извлечении элемента по ключу."""

    def __init__(self, *args):
        """Переопределение нужного поля."""
        self.KeyError = 'Такого ключа нет!'

    def __str__(self):
        """Отображение в нужном формате."""
        return self.KeyError


class StatusCode(Exception):
    """Неверный код ответа."""

    def __init__(self, *args):
        """Переопределение нужного поля."""
        self.StatusCode = 'Код ответа не 200!'

    def __str__(self):
        """Отображение в нужном формате."""
        return self.StatusCode


class TelegramError(telegram.TelegramError):
    """Ошибка при отправке сообщения."""

    def __init__(self, *args):
        """Переопределение нужного поля."""
        self.TelegramError = 'Ошибка приотправке сообщения!'

    def __str__(self):
        """Отображение в нужном формате."""
        return self.TelegramError


class RequestException(RequestException):
    """Ошибка запроса."""

    def __init__(self, *args):
        """Переопределение нужного поля."""
        self.RequestException = 'Something wrong'

    def __str__(self):
        """Отображение в нужном формате."""
        return self.RequestException


class JSONDecodeError(Exception):
    """Ошибка приведения к нужному формату данных."""

    def __init__(self, *args):
        """Переопределение нужного поля."""
        self.JSONDecodeError = 'Something wrong'

    def __str__(self):
        """Отображение в нужном формате."""
        return self.JSONDecodeError
