"""
Сервис для работы с книгами в Telegram-боте
Использует существующие репозитории из backend
"""
import sys
import os
from typing import List, Optional, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession

# Добавляем путь к backend для импорта моделей и репозиториев
sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))

# Импорты после добавления пути
from app.models.books import Book  # noqa: E402
from app.repositories.books import BookRepository  # noqa: E402


class BooksService:
    """Сервис для управления книгами через Telegram-бот"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.book_repo = BookRepository(db)

    # === BOOKS ===

    async def get_all_books(self) -> List[Book]:
        """Получить все книги"""
        return await self.book_repo.list()

    async def create_book(
        self,
        title: str,
        author: Optional[str] = None,
        genre: Optional[str] = None,
        language: Optional[str] = None,
        format: Optional[str] = None,
        review: Optional[str] = None,
        quotes: Optional[List[Dict[str, Any]]] = None,
        opinion: Optional[str] = None
    ) -> Book:
        """Создать новую книгу"""
        return await self.book_repo.create(
            title=title,
            author=author,
            genre=genre,
            language=language,
            format=format,
            review=review,
            quotes=quotes,
            opinion=opinion
        )

    async def get_book_by_id(self, book_id: str) -> Optional[Book]:
        """Получить книгу по ID"""
        return await self.book_repo.get_by_id(book_id)

    async def update_book(
        self,
        book_id: str,
        title: Optional[str] = None,
        author: Optional[str] = None,
        genre: Optional[str] = None,
        language: Optional[str] = None,
        format: Optional[str] = None,
        review: Optional[str] = None,
        quotes: Optional[List[Dict[str, Any]]] = None,
        opinion: Optional[str] = None
    ) -> Optional[Book]:
        """Обновить книгу"""
        update_data = {}
        if title is not None:
            update_data['title'] = title
        if author is not None:
            update_data['author'] = author
        if genre is not None:
            update_data['genre'] = genre
        if language is not None:
            update_data['language'] = language
        if format is not None:
            update_data['format'] = format
        if review is not None:
            update_data['review'] = review
        if quotes is not None:
            update_data['quotes'] = quotes
        if opinion is not None:
            update_data['opinion'] = opinion

        if not update_data:
            return await self.get_book_by_id(book_id)

        return await self.book_repo.update(book_id, **update_data)

    async def delete_book(self, book_id: str) -> bool:
        """Удалить книгу"""
        return await self.book_repo.delete(book_id)

    async def search_books(self, query: str) -> List[Book]:
        """Поиск книг по названию или автору"""
        all_books = await self.get_all_books()
        query_lower = query.lower()

        return [
            book for book in all_books
            if (query_lower in book.title.lower()) or
            (book.author and query_lower in book.author.lower())
        ]

    async def get_books_by_genre(self, genre: str) -> List[Book]:
        """Получить книги по жанру"""
        all_books = await self.get_all_books()
        return [
            book for book in all_books
            if book.genre and genre.lower() in book.genre.lower()
        ]

    async def get_books_by_language(self, language: str) -> List[Book]:
        """Получить книги по языку"""
        all_books = await self.get_all_books()
        return [
            book for book in all_books
            if book.language and language.lower() in book.language.lower()
        ]

    # === HELPER METHODS ===

    async def format_book_info(self, book: Book) -> str:
        """Форматировать информацию о книге для отображения"""
        info = f"📚 *{book.title}*\n"

        if book.author:
            info += f"✍️ Автор: {book.author}\n"

        if book.genre:
            info += f"🎭 Жанр: {book.genre}\n"

        if book.language:
            info += f"🌐 Язык: {book.language}\n"

        if book.format:
            info += f"📖 Формат: {book.format}\n"

        if book.review:
            info += f"\n📝 *Рецензия:*\n_{book.review}_\n"

        if book.opinion:
            info += f"\n💭 *Мнение:*\n_{book.opinion}_\n"

        if book.quotes:
            info += f"\n💬 *Цитаты ({len(book.quotes)}):*\n"
            for i, quote in enumerate(book.quotes[:3], 1):  # Показываем только первые 3
                quote_text = quote.get('text', '')
                page = quote.get('page')
                info += f"{i}. _{quote_text}_"
                if page:
                    info += f" (стр. {page})"
                info += "\n"

            if len(book.quotes) > 3:
                info += f"... и еще {len(book.quotes) - 3} цитат\n"

        return info

    async def get_all_genres(self) -> List[str]:
        """Получить все уникальные жанры"""
        all_books = await self.get_all_books()
        genres = set()

        for book in all_books:
            if book.genre:
                genres.add(book.genre)

        return sorted(list(genres))

    async def get_all_languages(self) -> List[str]:
        """Получить все уникальные языки"""
        all_books = await self.get_all_books()
        languages = set()

        for book in all_books:
            if book.language:
                languages.add(book.language)

        return sorted(list(languages))

    async def get_all_formats(self) -> List[str]:
        """Получить все уникальные форматы"""
        all_books = await self.get_all_books()
        formats = set()

        for book in all_books:
            if book.format:
                formats.add(book.format)

        return sorted(list(formats))

    async def add_quote_to_book(
        self,
        book_id: str,
        quote_text: str,
        page: Optional[int] = None
    ) -> Optional[Book]:
        """Добавить цитату к книге"""
        book = await self.get_book_by_id(book_id)
        if not book:
            return None

        quotes = book.quotes or []
        new_quote = {"text": quote_text}
        if page:
            new_quote["page"] = page

        quotes.append(new_quote)
        return await self.update_book(book_id, quotes=quotes)

    async def commit(self):
        """Зафиксировать изменения в БД"""
        await self.db.commit()

    async def rollback(self):
        """Откатить изменения в БД"""
        await self.db.rollback()
