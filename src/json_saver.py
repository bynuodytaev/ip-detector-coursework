import json


class JsonSaver:
    """Класс для сохранения данных в JSON формат."""

    @staticmethod
    def to_json_string(data: dict) -> str:
        """
        Конвертирует словарь в JSON-строку.

        :param data: Словарь с данными
        :return: JSON-строка
        """
        return json.dumps(data, indent=2, ensure_ascii=False)

    @staticmethod
    def to_json_bytes(data: dict) -> bytes:
        """
        Конвертирует словарь в JSON-байты (для отправки на сервер).

        :param data: Словарь с данными
        :return: Байты JSON в кодировке UTF-8
        """
        json_string = JsonSaver.to_json_string(data)
        return json_string.encode('utf-8')