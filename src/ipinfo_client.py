import requests
import os
from dotenv import load_dotenv


class IpinfoClient:
    """Клиент для получения геоданных по IP через сервис ipinfo.io"""

    def __init__(self, api_token: str, timeout: int = 10):
        """
        Инициализация клиента.

        :param api_token: Токен доступа к API ipinfo.io
        :param timeout: Таймаут запроса в секундах
        """
        self.api_token = api_token
        self.timeout = timeout
        self.base_url = "https://ipinfo.io"

    def get_geo_info(self, ip_address: str) -> dict:
        """
        Получает геоданные по IP-адресу.

        :param ip_address: IP-адрес для поиска
        :return: Словарь с геоданными (город, регион, страна и т.д.)
        :raises: ConnectionError при проблемах с сетью
        """
        try:
            url = f"{self.base_url}/{ip_address}/geo?token={self.api_token}"
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Не удалось получить геоданные: {e}")