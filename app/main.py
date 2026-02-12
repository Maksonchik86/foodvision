import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import logging
from app.config import settings 
from app.bot import setup_bot

# Настройка логирования
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Создаем экземпляр бота
bot_application = setup_bot()

# Создаем FastAPI приложение
app = FastAPI(title="Food Vision Bot", debug=settings.DEBUG)

@app.get("/")
async def root():
    """Корневой эндпоинт для проверки работы."""
    return {
        "status": "active",
        "service": "Food Vision Bot",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Эндпоинт для проверки здоровья сервиса."""
    return {"status": "healthy"}

@app.post(f"/webhook/{settings.TELEGRAM_BOT_TOKEN}")
async def telegram_webhook(request: Request):
    """Эндпоинт для вебхука от Telegram."""
    try:
        # Получаем обновление от Telegram
        update_data = await request.json()
        
        # Создаем Update объект
        update = Update.de_json(update_data, bot_application.bot)
        
        # Обрабатываем обновление
        await bot_application.process_update(update)
        
        return JSONResponse(content={"status": "ok"})
        
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        raise HTTPException(status_code=400, detail="Invalid update")

@app.on_event("startup")
async def on_startup():
    """Действия при запуске приложения."""
    logger.info("Starting Food Vision Bot...")
    
    # Инициализируем бота
    await bot_application.initialize()
    await bot_application.start()
    await bot_application.updater.start_polling()
    
    logger.info(f"Bot is ready! Webhook URL: /webhook/{settings.TELEGRAM_BOT_TOKEN}")

@app.on_event("shutdown")
async def on_shutdown():
    """Действия при остановке приложения."""
    logger.info("Shutting down Food Vision Bot...")
    
    # Останавливаем бота
    await bot_application.updater.stop()
    await bot_application.stop()
    await bot_application.shutdown()
    
    logger.info("Bot stopped successfully.")

if __name__ == "__main__":
    # Запуск сервера напрямую (для отладки)
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.BOT_PORT,
        reload=settings.DEBUG
    )