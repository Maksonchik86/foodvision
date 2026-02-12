import base64
import json
import httpx
from app.config import settings

async def analyze_image_for_food(image_bytes: bytes) -> dict:
    """
    Анализирует изображение еды через OpenAI GPT-4 Vision.
    Возвращает словарь с результатами анализа.
    """
    # Кодируем изображение в base64
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    
    # Промпт для анализа еды
    prompt = """Ты - профессиональный диетолог. Проанализируй изображение еды.
    Верни ответ ТОЛЬКО в формате JSON без каких-либо пояснений:
    {
        "description": "краткое описание блюда на русском",
        "calories": число,
        "protein": число,
        "fat": число,
        "carbs": число
    }"""
    
    # Подготавливаем запрос к OpenAI API
    headers = {
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 500
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # Извлекаем JSON из ответа
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            json_str = content[json_start:json_end]
            
            return json.loads(json_str)
            
    except Exception as e:
        return {
            "description": f"Ошибка анализа: {str(e)}",
            "calories": 0,
            "protein": 0,
            "fat": 0,
            "carbs": 0
        }