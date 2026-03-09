# RAG-бот для Eternum Nexus

Проектная работа по созданию RAG-бота с уникальной базой знаний на основе вселенной Eternum Nexus (трансформированный Lineage 2).

## Быстрый старт

### 1. Установка зависимостей

```bash
# Создание виртуального окружения
make setup

# Или вручную:
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Просмотр базы знаний

```bash
# Посмотреть список документов
make show-docs

# Посмотреть словарь замен терминов
make show-terms
```

### 3. Создание векторного индекса

```bash
# Построить индекс (займет ~2 минуты)
make build-index

# Или вручную:
source .venv/bin/activate
python scripts/build_index.py
```

### 4. Получение API ключа (для RAG-бота)

Бот поддерживает 3 провайдера LLM (автоматически выбирает доступный):

**YandexGPT (рекомендуется для России):**
```bash
export YANDEX_API_KEY="your-api-key"
export YANDEX_FOLDER_ID="your-folder-id"
make run-bot
```

**Google Gemini (бесплатный tier, без привязки карты):**
```bash
export GOOGLE_API_KEY="your-api-key"
make run-bot
```

**OpenAI (платный):**
```bash
export OPENAI_API_KEY="your-api-key"
make run-bot
```

### 5. Тестирование поиска

```bash
# Запустить интерактивный поиск
make test-search

# Или вручную:
source .venv/bin/activate
python scripts/test_search.py
```

## Структура проекта

```
architecture-rag/
├── data/
│   └── raw/                    # 32 оригинальных документа (Lineage 2)
├── knowledge_base/             # 32 трансформированных документа (Eternum Nexus)
├── chroma_db/                  # Векторный индекс ChromaDB
├── models_cache/               # Кэш модели эмбеддингов
├── scripts/
│   ├── replace_terms.py        # Замена терминов
│   ├── build_index.py          # Построение индекса
│   └── test_search.py          # Тестирование поиска
├── terms_map.json              # Словарь замен (123 термина)
├── Makefile                    # Быстрые команды
└── requirements.txt            # Зависимости Python
```

## Основные команды

### Работа с окружением

```bash
make setup          # Установить зависимости
make clean          # Очистить кэши и индексы
make clean-all      # Полная очистка (включая .venv)
```

### Работа с базой знаний

```bash
make show-docs      # Показать список документов
make show-terms     # Показать словарь замен
make rebuild-kb     # Пересоздать базу знаний из raw/
```

### Работа с индексом

```bash
make build-index    # Создать векторный индекс
make test-search    # Интерактивный поиск
make stats          # Статистика проекта
```

### Разработка

```bash
make help           # Показать все команды
```

## База знаний Eternum Nexus

### Что это?

Уникальная база знаний созданная путем трансформации Lineage 2:
- **32 документа** (~32,000 слов)
- **123 термина** заменены на вымышленные
- **Категории**: расы, классы, локации, системы, боссы

### Примеры замен:

| Оригинал | Eternum Nexus |
|----------|---------------|
| Lineage 2 | Eternum Nexus |
| Humans | Aetherians |
| Adena | Stellarium |
| Aden | Valorheim |
| Dragon | Wyrm |
| Antharas | Terragorax |

### Зачем трансформация?

LLM не знает вселенную Eternum Nexus - это гарантирует, что ответы идут только из RAG, а не из "памяти" модели.

## Векторный индекс

### Параметры:

- **Модель эмбеддингов**: all-MiniLM-L6-v2 (384 dim)
- **Векторная БД**: ChromaDB
- **Чанков**: 228 (из 32 документов)
- **Chunk size**: 500 символов
- **Overlap**: 50 символов

### Статистика:

```
Время индексации: 2.21 сек
Скорость: ~103 чанка/сек
Размер индекса: ~2 MB
Латентность поиска: <10ms
```

## Технический стек

### Python библиотеки:

- **langchain-community** - RAG фреймворк
- **chromadb** - векторная база данных
- **sentence-transformers** - модели эмбеддингов
- **langchain-text-splitters** - разбиение текста

### Модели:

- **Эмбеддинги**: sentence-transformers/all-MiniLM-L6-v2
- **LLM**: YandexGPT, Google Gemini 1.5 Flash, или OpenAI GPT-4o-mini
  - YandexGPT: Бесплатный грант (хорош для русского языка)
  - Gemini: Бесплатный tier (60 RPM, 1M tokens/день)
  - OpenAI: Платный (требует пополнения баланса)

## Получение API ключа

### YandexGPT (рекомендуется для России)

1. Перейдите: https://console.cloud.yandex.ru/
2. Создайте сервисный аккаунт и получите API ключ
3. Скопируйте Folder ID вашего каталога
4. Установите:
   ```bash
   export YANDEX_API_KEY="your-key"
   export YANDEX_FOLDER_ID="your-folder-id"
   ```
5. Запустите: `make run-bot`

**Преимущества:**
- Отличная поддержка русского языка
- Бесплатный грант для начала работы
- Данные хранятся в России

См. подробную инструкцию: https://cloud.yandex.ru/docs/yandexgpt/

### Google Gemini (бесплатный tier)

1. Получите ключ: https://makersuite.google.com/app/apikey
2. Установите: `export GOOGLE_API_KEY="your-key"`
3. Запустите: `make run-bot`

**Преимущества:**
- Полностью бесплатный tier (60 RPM)
- Не требует привязки карты
- Достаточно для учебных проектов

Детали: https://ai.google.dev/gemini-api/docs

### OpenAI (платный)

1. Получите ключ: https://platform.openai.com/api-keys
2. Установите: `export OPENAI_API_KEY="your-key"`
3. Запустите: `make run-bot`

Бот автоматически выберет доступный API по приоритету: YandexGPT → Gemini → OpenAI.

