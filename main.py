import os
from dotenv import load_dotenv
from src.ipify_client import IpifyClient
from src.ipinfo_client import IpinfoClient
from src.json_saver import JsonSaver
from src.yandex_uploader import YandexDiskUploader
from datetime import datetime


def main():
    """Точка входа в программу."""
    # Загружаем токены из .env
    load_dotenv()
    
    # 1. Получаем IP
    ip_client = IpifyClient()
    ip = ip_client.get_public_ip()
    print(f"✓ Твой IP: {ip}")
    
    # 2. Получаем геоданные
    token = os.getenv('IPINFO_TOKEN')
    geo_client = IpinfoClient(api_token=token)
    geo_data = geo_client.get_geo_info(ip)
    
    print(f"✓ Город: {geo_data.get('city', 'не определён')}")
    print(f"✓ Регион: {geo_data.get('region', 'не определён')}")
    print(f"✓ Страна: {geo_data.get('country', 'не определён')}")
    
    # 3. Формируем итоговый отчёт
    report = {
        "ip": ip,
        "geo_info": geo_data,
        "timestamp": datetime.now().isoformat()
    }
    
    # 4. Конвертируем в JSON (байты)
    json_bytes = JsonSaver.to_json_bytes(report)
    print(f"✓ JSON создан ({len(json_bytes)} байт)")
    
    # 5. Загружаем на Яндекс.Диск
    yandex_token = os.getenv('YANDEX_DISK_TOKEN')
    folder_name = "ip-detector-coursework"
    remote_path = f"disk:/{folder_name}/report_{ip}.json"
    
    uploader = YandexDiskUploader(oauth_token=yandex_token)
    
    print(f"📁 Создаю папку: {folder_name}...")
    uploader.create_folder(folder_name)
    
    print(f"☁️ Загружаю файл на Яндекс.Диск...")
    success = uploader.upload_file(json_bytes, remote_path)
    
    if success:
        print(f"✅ Файл успешно загружен: {remote_path}")
    else:
        print(f"❌ Ошибка загрузки файла")


if __name__ == "__main__":
    main()