import asyncio
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .services import fetch_yandex_data

logger = logging.getLogger(__name__)
request_counter = 0
semaphore = asyncio.Semaphore(4)

@csrf_exempt
async def handle_request(request):
    global request_counter
    if request.method != 'POST':
        return JsonResponse({"error": "Invalid method"}, status=405)
    try:
        data = json.loads(request.body)
        query = data.get("query")
        if not query:
            return JsonResponse({"error": "Missing 'query' field"}, status=400)
        
        request_counter += 1
        async with semaphore:
            result = await fetch_yandex_data(query, request_counter)
        
        return JsonResponse(result, status=200)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        return JsonResponse({"error": "Internal server error"}, status=500)