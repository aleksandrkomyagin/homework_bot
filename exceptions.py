from requests.exceptions import RequestException


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
