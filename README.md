# AI agent on Django

Этот проект на Django предоставляет API для взаимодействия с сервисами поиска Yandex и GPT для генерации ответов. Цель проекта — обрабатывать запросы пользователей, получать данные с поиска Yandex и использовать GPT для генерации подробного ответа.

## Возможности

- **Асинхронная обработка запросов**: Используется Python `asyncio` для эффективных неблокирующих сетевых запросов.
- **API поиска Yandex**: Получение результатов поиска по запросам пользователей.
- **Интеграция с YandexGPT**: Отправка результатов поиска в модель GPT от Yandex для генерации ответа.
- **Обработка ошибок**: Подробная обработка ошибок с соответствующими HTTP статусами.
- **Ограничение запросов**: Используется семафор для управления параллельными запросами и предотвращения перегрузки внешних сервисов.

## Технологии

- **Django**: Веб-фреймворк для обработки API запросов.
- **AsyncIO**: Для асинхронной обработки сетевых запросов.
- **Aiohttp**: Для отправки HTTP запросов асинхронно к внешним API.
- **Yandex Cloud API**: Интеграция с поисковым и GPT API от Yandex.
- **Dotenv**: Для безопасного хранения переменных окружения.

## Установка

### Требования

- Python 3.8+
- Django
- Аккаунт в Yandex Cloud с доступом к Yandex Search API и Yandex GPT API.

### Инструкция по установке

1. Клонируй репозиторий:

   ```bash
   git clone https://github.com/yourusername/django-yandexgpt-api.git
   cd django-yandexgpt-api

# Установка и настройка проекта

## Установите зависимости

Для начала установите все необходимые зависимости из файла `requirements.txt`:

   ```bash
   pip install -r requirements.txt

## Создание файла `.env` и добавление ключей от Yandex API

В корневой директории проекта создайте файл `.env` и добавьте в него свои ключи от Yandex API:

```env
YANDEX_SEARCH_API=your_yandex_search_api_key
YANDEX_GPT_API=your_yandex_gpt_api_key
FOLDER_ID=your_yandex_folder_id

## Примените миграции (если необходимо):

- python manage.py migrate

## Запусти сервер Django:

- python manage.py runserver

# Тестирование API
## Чтобы протестировать API, отправь POST запрос на эндпоинт /handle_request/ с таким JSON телом:

{
  "query": "Какая столица Франции?"
}

Ответ:

{
  "id": 1,
  "answer": 42,
  "reasoning": "Ответ сгенерирован YandexGPT.",
  "sources": [
    "https://yandex.ru",
    "https://ya.ru"
  ]
}

## Лицензия
- Этот проект лицензирован по лицензии MIT — подробности см. в файле LICENSE.
