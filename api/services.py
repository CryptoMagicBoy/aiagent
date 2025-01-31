import aiohttp
import os
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def fetch_yandex_data(query_text, req_id):
    load_dotenv()
    headers = {"Authorization": f"Api-Key {os.getenv('YANDEX_SEARCH_API')}"}
    payload = {"messages": [{"content": query_text, "role": "user"}]}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"https://ya.ru/search/xml/generative?folderid={os.getenv('FOLDER_ID')}",
                                    headers=headers, json=payload) as resp:
                if resp.status != 200:
                    logger.error(f"Search API error: {resp.status}")
                    return {"error": "Search API failed", "status": resp.status}
                
                data = await resp.json()
                info_text = data.get('message', {}).get('content', "")
                sources = data.get('links', [])
                if not info_text:
                    return {"error": "Empty search response"}
        except aiohttp.ClientError as e:
            logger.error(f"Network error: {str(e)}")
            return {"error": "Network issue"}
        
        return await query_gpt(info_text, query_text, sources, req_id)

async def query_gpt(info_text, query_text, sources, req_id):
    payload = {
        "modelUri": f"gpt://{os.getenv('FOLDER_ID')}/yandexgpt/latest",
        "completionOptions": {"temperature": 0.3, "maxTokens": 1000},
        "messages": [
            {"role": "system", "text": "Ты отвечаешь на вопросы об Университете ИТМО."},
            {"role": "user", "text": f"{info_text}\nВОПРОС: {query_text}"}
        ]
    }
    headers = {"Authorization": f"Api-Key {os.getenv('YANDEX_GPT_API')}", "Accept": "application/json"}
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post("https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
                                    headers=headers, json=payload) as resp:
                if resp.status != 200:
                    return {"error": "GPT API error", "status": resp.status}
                
                result = await resp.json()
                answer_text = result.get('result', {}).get('alternatives', [{}])[0].get('message', {}).get('text', "")
                if not answer_text:
                    return {"error": "GPT returned no answer"}
        except aiohttp.ClientError as e:
            return {"error": f"GPT request failed: {str(e)}"}
    
    return {
        "id": req_id,
        "answer": extract_answer(answer_text),
        "reasoning": f"{answer_text}\nОтвет подготовлен YandexGPT.",
        "sources": sources[:3]
    }

def extract_answer(text):
    try:
        return int(text[:2]) if text[:2].isdigit() else (int(text[:1]) if text[:1].isdigit() else None)
    except ValueError:
        return None