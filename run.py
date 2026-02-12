#!/usr/bin/env python3
"""
Скрипт для запуска Food Vision Bot.
Использование: python run.py
"""

import os
import sys
import subprocess
import time

def check_dependencies():
    """Проверяет установлены ли все зависимости."""
    print("🔍 Проверяем зависимости...")
    
    required_packages = [
        "fastapi",
        "uvicorn",
        "python-telegram-bot",
        "httpx",
        "pydantic",
        "python-dotenv"
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Отсутствуют пакеты: {', '.join(missing)}")
        print("Устанавливаем...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Зависимости установлены")
    else:
        print("✅ Все зависимости установлены")

def check_env_file():
    """Проверяет наличие и корректность .env файла."""
    print("🔍 Проверяем файл .env...")
    
    env_file = ".env"
    example_file = ".env.example"
    
    # Если нет .env, но есть .env.example
    if not os.path.exists(env_file) and os.path.exists(example_file):
        print("⚠️  Файл .env не найден!")
        print(f"Создайте его на основе {example_file}")
        print("И заполните TELEGRAM_BOT_TOKEN и OPENAI_API_KEY")
        return False
    
    if not os.path.exists(env_file):
        print("❌ Файл .env не найден!")
        print("Создайте файл .env с переменными окружения")
        return False
    
    # Читаем .env для проверки
    with open(env_file, 'r') as f:
        content = f.read()
    
    if "your_bot_token_here" in content or "your_openai_api_key_here" in content:
        print("❌ В файле .env остались значения по умолчанию!")
        print("Замените your_bot_token_here и your_openai_api_key_here на реальные значения")
        return False
    
    print("✅ Файл .env проверен")
    return True

def main():
    """Основная функция запуска."""
    print("=" * 50)
    print("🚀 Food Vision Bot - Запуск")
    print("=" * 50)
    
    # Проверяем зависимости
    check_dependencies()
    
    # Проверяем .env файл
    if not check_env_file():
        print("\n❌ Не удалось запустить бота. Исправьте ошибки выше.")
        input("Нажмите Enter для выхода...")
        sys.exit(1)
    
    print("\n✅ Все проверки пройдены!")
    print("Запускаем сервер...")
    print(f"📡 Сервер будет доступен по адресу: http://localhost:8000")
    print(f"📋 Документация API: http://localhost:8000/docs")
    print("🛑 Для остановки нажмите Ctrl+C\n")
    
    # Импортируем и запускаем приложение
    try:
        import uvicorn
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n👋 Остановка сервера...")
    except Exception as e:
        print(f"\n❌ Ошибка запуска: {e}")
        input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    main()