import requests
import os


class YandexDiskUploader:
    """Клиент для загрузки файлов на Яндекс.Диск через REST API."""

    def __init__(self, oauth_token: str, timeout: int = 10):
        """
        Инициализация клиента.

        :param oauth_token: OAuth-токен Яндекс.Диска
        :param timeout: Таймаут запроса в секундах
        """
        self.oauth_token = oauth_token
        self.timeout = timeout
        self.base_url = "https://cloud-api.yandex.net/v1/disk"
        self.headers = {
            'Authorization': f'OAuth {self.oauth_token}',
            'Content-Type': 'application/json'
        }

    def create_folder(self, folder_name: str) -> bool:
        """
        Создаёт папку на Яндекс.Диске.

        :param folder_name: Имя папки
        :return: True если успешно
        """
        url = f"{self.base_url}/resources"
        params = {'path': f'disk:/{folder_name}'}
        
        try:
            response = requests.put(url, headers=self.headers, params=params, timeout=self.timeout)
            # 201 = создана, 409 = уже существует
            return response.status_code in (201, 409)
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Ошибка создания папки: {e}")
            return False

    def get_upload_url(self, remote_path: str) -> str:
        """
        Получает ссылку для загрузки файла.

        :param remote_path: Путь к файлу на Диске
        :return: URL для загрузки
        """
        url = f"{self.base_url}/resources/upload"
        params = {
            'path': remote_path,
            'overwrite': 'true'
        }
        
        response = requests.get(url, headers=self.headers, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()['href']

    def upload_file(self, file_content: bytes, remote_path: str) -> bool:
        """
        Загружает файл на Яндекс.Диск.

        :param file_content: Содержимое файла в байтах
        :param remote_path: Путь к файлу на Диске
        :return: True если успешно
        """
        try:
            upload_url = self.get_upload_url(remote_path)
            response = requests.put(upload_url, data=file_content, timeout=self.timeout)
            return response.status_code in (200, 201)
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Ошибка загрузки файла: {e}")
            return False