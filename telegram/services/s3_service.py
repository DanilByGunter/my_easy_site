"""
Сервис для работы с S3 хранилищем Яндекс.Облако
"""
import os
import uuid
import logging
from typing import Optional
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
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
            self.s3_client = None
        else:
            self.configured = True
            try:
                # Создаем S3 клиент для Яндекс.Облако
                self.s3_client = boto3.client(
                    's3',
                    endpoint_url=self.endpoint_url,
                    aws_access_key_id=self.access_key,
                    aws_secret_access_key=self.secret_key,
                    region_name=self.region
                )
            except Exception as e:
                logger.error(f"Failed to create S3 client: {e}")
                self.configured = False
                self.s3_client = None

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
        if not self.configured or not self.s3_client:
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

            # Загружаем файл в S3 с публичным доступом
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=file_data,
                ContentType=f'image/{file_extension}',
                ACL='public-read'
            )

            # Формируем публичный URL
            upload_url = f"{self.endpoint_url}/{self.bucket_name}/{s3_key}"
            logger.info(f"Photo uploaded to S3: {upload_url}")
            return upload_url

        except NoCredentialsError:
            logger.error("S3 credentials not found")
            return None
        except ClientError as e:
            logger.error(f"S3 client error uploading photo: {e}")
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
        if not self.configured or not self.s3_client or not photo_url:
            return False

        try:
            # Проверяем, что URL содержит наш bucket
            if self.bucket_name in photo_url:
                # Извлекаем ключ из URL
                s3_key = photo_url.replace(f"{self.endpoint_url}/{self.bucket_name}/", "")

                # Удаляем файл из S3
                self.s3_client.delete_object(
                    Bucket=self.bucket_name,
                    Key=s3_key
                )

                logger.info(f"Photo deleted from S3: {photo_url}")
                return True

        except ClientError as e:
            logger.error(f"S3 client error deleting photo: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error deleting photo: {e}")
            return False

        return False
