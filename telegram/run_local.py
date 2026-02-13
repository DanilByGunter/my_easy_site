#!/usr/bin/env python3
"""
Скрипт для локального запуска бота (для разработки)
"""
import sys
import os

# Добавляем путь к backend для локальной разработки
backend_path = os.path.join(os.path.dirname(__file__), '../backend')
sys.path.insert(0, backend_path)

# Запускаем бота
if __name__ == "__main__":
    from bot import main
    import asyncio

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ Бот остановлен пользователем")
    except Exception as e:
        print(f"❌ Критическая ошибка при запуске: {e}")
        sys.exit(1)
