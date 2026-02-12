import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from app.config import settings
from app.vision import analyze_image_for_food

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start."""
    user = update.effective_user
    welcome_text = (
        f"Привет, {user.first_name}! 👋\n\n"
        "Я бот для анализа еды по фото. 🍎📸\n"
        "Просто отправь мне фото своего блюда, и я определю:\n"
        "• Описание блюда\n"
        "• Калории (ккал)\n"
        "• Белки (г)\n"
        "• Жиры (г)\n"
        "• Углеводы (г)\n\n"
        "Отправь фото и увидишь! 🍕🥗"
    )
    await update.message.reply_text(welcome_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help."""
    help_text = (
        "📋 **Доступные команды:**\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать эту справку\n\n"
        "📸 **Как использовать:**\n"
        "1. Сделай фото еды\n"
        "2. Отправь фото в этот чат\n"
        "3. Получи анализ КБЖУ через 10-20 секунд\n\n"
        "⚠️ **Примечания:**\n"
        "• Фото должно быть четким\n"
        "• Еда должна занимать большую часть кадра\n"
        "• Результаты приблизительные"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик фотографий."""
    try:
        await update.message.reply_text("🔍 Анализирую фото... Это займет 10-20 секунд.")
        
        # Получаем фото наибольшего качества
        photo_file = await update.message.photo[-1].get_file()
        image_bytes = await photo_file.download_as_bytearray()
        
        # Анализируем изображение
        analysis = await analyze_image_for_food(image_bytes)
        
        # Форматируем ответ
        response = (
            f"🍽 **Результаты анализа:**\n\n"
            f"📝 **Описание:** {analysis['description']}\n\n"
            f"⚖️ **Пищевая ценность (приблизительно):**\n"
            f"• Калории: {analysis['calories']} ккал\n"
            f"• Белки: {analysis['protein']} г\n"
            f"• Жиры: {analysis['fat']} г\n"
            f"• Углеводы: {analysis['carbs']} г\n\n"
            f"💡 *Результаты могут отличаться от реальных значений*"
        )
        
        await update.message.reply_text(response, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Ошибка обработки фото: {e}")
        await update.message.reply_text("❌ Произошла ошибка при анализе фото. Попробуйте еще раз.")

def setup_bot():
    """Настраивает и возвращает экземпляр бота."""
    # Создаем Application
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    
    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    return application