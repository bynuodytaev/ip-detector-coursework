import requests


class IpifyClient:
    """Клиент для получения публичного IP-адреса через сервис ipify."""

    def __init__(self, timeout: int = 10):
        """
        Инициализация клиента.

        :param timeout: Таймаут запроса в секундах
        """
        self.timeout = timeout
        self.api_url = "https://api64.ipify.org?format=json"

    def get_public_ip(self) -> str:
        """
        Получает публичный IP-адрес пользователя.

        :return: IP-адрес в виде строки
        :raises: ConnectionError, Timeout при проблемах с сетью
        """
        try:
            response = requests.get(self.api_url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            return data['ip']
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Не удалось получить IP-адрес: {e}")