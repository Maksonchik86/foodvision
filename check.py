import os
import sys

print("=" * 50)
print("ДИАГНОСТИКА СТРУКТУРЫ ПРОЕКТА")
print("=" * 50)

# 1. Текущая директория
current_dir = os.getcwd()
print(f"1. Текущая директория: {current_dir}")
print(f"   Папка 'app' существует: {os.path.exists('app')}")

# 2. Содержимое текущей директории
print("\n2. Содержимое текущей папки:")
for item in os.listdir('.'):
    if os.path.isdir(item):
        print(f"   📁 {item}/")
    else:
        print(f"   📄 {item}")

# 3. Содержимое папки app
if os.path.exists('app'):
    print("\n3. Содержимое папки 'app':")
    if not os.listdir('app'):
        print("   ❗ Папка 'app' ПУСТАЯ!")
    else:
        for item in os.listdir('app'):
            path = os.path.join('app', item)
            if os.path.isdir(path):
                print(f"   📁 {item}/")
            else:
                print(f"   📄 {item}")
        
    # 4. Проверка __init__.py
    init_file = os.path.join('app', '__init__.py')
    print(f"\n4. Файл __init__.py существует: {os.path.exists(init_file)}")
    
    # 5. Проверка bot.py
    bot_file = os.path.join('app', 'bot.py')
    print(f"5. Файл bot.py существует: {os.path.exists(bot_file)}")
    
    # 6. Проверка импорта
    print("\n6. Тест импорта модулей:")
    sys.path.insert(0, current_dir)
    
    try:
        from app import config
        print("   ✅ app.config - УСПЕХ")
    except ImportError as e:
        print(f"   ❌ app.config - ОШИБКА: {e}")
    
    try:
        from app import bot
        print("   ✅ app.bot - УСПЕХ")
    except ImportError as e:
        print(f"   ❌ app.bot - ОШИБКА: {e}")
else:
    print("\n❌ КРИТИЧЕСКАЯ ОШИБКА: Папки 'app' не существует!")
    print("   Вы находитесь не в той директории.")

print("\n" + "=" * 50)
print("РЕКОМЕНДАЦИИ:")
print("1. Запускайте бота ИЗ папки food_vision_bot")
print("2. Команда: python -m uvicorn app.main:app --reload")
print("=" * 50)