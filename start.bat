@echo off
chcp 65001 > nul
title Food Vision Bot Launcher
echo ========================================
echo   🚀 Food Vision Bot - Запуск
echo ========================================
echo.

rem Проверяем Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден!
    echo Установите Python 3.8 или выше
    echo Скачать: https://www.python.org/downloads/
    pause
    exit /b 1
)

rem Проверяем pip
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip не найден!
    echo Установите pip для Python
    pause
    exit /b 1
)

rem Устанавливаем зависимости если нужно
if not exist "venv" (
    echo 🔧 Создаем виртуальное окружение...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo 📦 Устанавливаем зависимости...
    pip install -r requirements.txt > install.log 2>&1
    if errorlevel 1 (
        echo ❌ Ошибка установки зависимостей!
        type install.log
        del install.log
        pause
        exit /b 1
    )
    del install.log
) else (
    call venv\Scripts\activate.bat
)

rem Запускаем бота
echo.
echo ✅ Все готово!
echo 🚀 Запускаем Food Vision Bot...
echo.
echo 📡 Сервер: http://localhost:8000
echo 📋 Документация: http://localhost:8000/docs
echo 🛑 Для остановки закройте это окно или нажмите Ctrl+C
echo.
echo ========================================

python run.py

pause