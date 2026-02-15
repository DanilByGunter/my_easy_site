"""
Сервис для работы с S3 хранилищем Яндекс.Облако
"""
import os
import uuid
import logging
import hashlib
import hmac
import datetime
from typing import Optional
import aiohttp
from aiogram import Bot
from aiogram.types import PhotoSize

logger = logging.getLogger(__name__)


class S3Service:
    """Сервис для загрузки файлов в S3 Яндекс.Облако"""

    def __init__(self):
        self.endpoint_url = os.getenv('S3_ENDPOINT_URL', 'https://storage.yandexcloud.net')
        self.access_key = os.getenv('S3_ACCESS_KEY')
        self.secret_key = os.getenv('S3_SECRET_KEY')
        self.bucket_name = os.getenv('S3_BUCKET_NAME')
        self.region = 'ru-central1'

        if not all([self.access_key, self.secret_key, self.bucket_name]):
            logger.warning("S3 credentials not configured. Photo upload will be disabled.")
            self.configured = False
        else:
            self.configured = True

    def _create_signature(self, method: str, url: str, headers: dict, payload: bytes, amz_date: str) -> str:
        """Создать AWS Signature Version 4 для Яндекс.Облако"""
        # Используем переданный amz_date
        date_stamp = amz_date[:8]  # Первые 8 символов YYYYMMDD

        # Создаем canonical request
        canonical_uri = url.replace(self.endpoint_url, '')
        canonical_querystring = ''
        canonical_headers = '\n'.join([f'{k.lower()}:{v}' for k, v in sorted(headers.items())]) + '\n'
        signed_headers = ';'.join([k.lower() for k in sorted(headers.keys())])
        payload_hash = hashlib.sha256(payload).hexdigest()

        canonical_request = f"{method}\n{canonical_uri}\n{canonical_querystring}\n{canonical_headers}\n{signed_headers}\n{payload_hash}"

        # Создаем string to sign
        algorithm = 'AWS4-HMAC-SHA256'
        credential_scope = f"{date_stamp}/{self.region}/s3/aws4_request"
        string_to_sign = f"{algorithm}\n{amz_date}\n{credential_scope}\n{hashlib.sha256(canonical_request.encode()).hexdigest()}"

        # Создаем signing key
        def sign(key, msg):
            return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

        k_date = sign(('AWS4' + self.secret_key).encode('utf-8'), date_stamp)
        k_region = sign(k_date, self.region)
        k_service = sign(k_region, 's3')
        k_signing = sign(k_service, 'aws4_request')

        # Создаем подпись
        signature = hmac.new(k_signing, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

        # Создаем authorization header
        authorization_header = f"{algorithm} Credential={self.access_key}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}"

        return authorization_header

    async def upload_photo(self, bot: Bot, photo: PhotoSize, folder: str = "vinyl") -> Optional[str]:
        """
        Загрузить фото в S3 Яндекс.Облако и вернуть URL

        Args:
            bot: Экземпляр бота для скачивания файла
            photo: Объект фото из Telegram
            folder: Папка в S3 для сохранения

        Returns:
            URL загруженного файла или None в случае ошибки
        """
        if not self.configured:
            logger.error("S3 credentials not configured")
            return None

        try:
            # Получаем файл из Telegram
            file = await bot.get_file(photo.file_id)
            file_path = file.file_path

            # Генерируем уникальное имя файла
            file_extension = file_path.split('.')[-1] if '.' in file_path else 'jpg'
            unique_filename = f"{uuid.uuid4()}.{file_extension}"
            s3_key = f"{folder}/{unique_filename}"

            # Скачиваем файл из Telegram
            file_data_io = await bot.download_file(file_path)

            # Получаем байты из BytesIO объекта
            file_data = file_data_io.getvalue()

            # Формируем URL для загрузки
            upload_url = f"{self.endpoint_url}/{self.bucket_name}/{s3_key}"

            # Подготавливаем заголовки с x-amz-date заранее
            now = datetime.datetime.utcnow()
            amz_date = now.strftime('%Y%m%dT%H%M%SZ')

            headers = {
                'Content-Type': f'image/{file_extension}',
                'Content-Length': str(len(file_data)),
                'x-amz-acl': 'public-read',
                'x-amz-date': amz_date
            }

            # Создаем подпись с уже включенным x-amz-date
            authorization = self._create_signature('PUT', upload_url, headers, file_data, amz_date)
            headers['Authorization'] = authorization

            # Загружаем файл через aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.put(upload_url, data=file_data, headers=headers) as response:
                    if response.status == 200:
                        logger.info(f"Photo uploaded to S3: {upload_url}")
                        return upload_url
                    else:
                        logger.error(f"Failed to upload photo. Status: {response.status}, Response: {await response.text()}")
                        return None

        except Exception as e:
            logger.error(f"Unexpected error uploading photo: {e}")
            return None

    async def delete_photo(self, photo_url: str) -> bool:
        """
        Удалить фото из S3 Яндекс.Облако

        Args:
            photo_url: URL фото для удаления

        Returns:
            True если удаление успешно, False иначе
        """
        if not self.configured or not photo_url:
            return False

        try:
            # Проверяем, что URL содержит наш bucket
            if self.bucket_name in photo_url:
                # Подготавливаем заголовки для DELETE запроса с x-amz-date заранее
                now = datetime.datetime.utcnow()
                amz_date = now.strftime('%Y%m%dT%H%M%SZ')

                headers = {
                    'x-amz-date': amz_date
                }

                # Создаем подпись для DELETE запроса
                authorization = self._create_signature('DELETE', photo_url, headers, b'', amz_date)
                headers['Authorization'] = authorization

                # Удаляем файл через aiohttp
                async with aiohttp.ClientSession() as session:
                    async with session.delete(photo_url, headers=headers) as response:
                        if response.status in [200, 204]:
                            logger.info(f"Photo deleted from S3: {photo_url}")
                            return True
                        else:
                            logger.error(f"Failed to delete photo. Status: {response.status}")
                            return False

        except Exception as e:
            logger.error(f"Unexpected error deleting photo: {e}")
            return False

        return False
