import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

class Settings(BaseSettings):
    """Настройки приложения."""
    TELEGRAM_BOT_TOKEN: str = ""
    OPENAI_API_KEY: str = ""
    BOT_PORT: int = 8000
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

def get_settings() -> Settings:
    """Возвращает экземпляр настроек."""
    settings = Settings()
    
    # Проверяем обязательные токены
    if not settings.TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN не найден в .env файле!")
    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY не найден в .env файле!")
    
    return settings

# Глобальный экземпляр настроек
settings = get_settings()