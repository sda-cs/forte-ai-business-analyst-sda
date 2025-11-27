Forte AI Business Analyst — MVP AI-помощник для сбора бизнес-требований

AI-ассистент, который ведёт диалог с сотрудником банка, уточняет детали проекта и автоматически формирует:

структурированный JSON с требованиями,

BRD-документ,

User Stories,

Use Case,

Mermaid-диаграмму бизнес-процесса.

Проект выполнен в рамках AI Hackathon ForteBank — Задача 4.


Цель проекта

Создать AI-агента, который заменяет ручной сбор бизнес-требований, ускоряет работу аналитиков и автоматически генерирует проектную документацию.


Основные возможности (MVP)

1. Диалоговый AI-агент

ведёт диалог с пользователем в формате чат-бота

задаёт уточняющие вопросы

анализирует ответы

формализует данные в структурированный набор требований


2. Автоматическая генерация документации

Система формирует:

JSON-структуру требований

BRD

User Stories

Use Case

Mermaid-диаграмму


3. Интерфейс

современный UI на Streamlit

фирменный стиль ForteBank

поддержка логотипа


Архитектура

Streamlit — интерфейс

Python — бизнес-логика

OpenAI API — генерация текста

Markdown/Mermaid — документация


Структура проекта

forte-ai-business-analyst-sda/

│── app.py               # Основной код Streamlit-приложения

│── requirements.txt     # Список зависимостей

│── forte_logo.png       # Логотип для интерфейса

│── README.md            # Описание проекта

└── .env                 # Локальный файл с OPENAI_API_KEY (НЕ публикуется)


Установка и запуск

Клонировать репозиторий

git clone https://github.com/sda-cs/forte-ai-business-analyst-sda

cd forte-ai-business-analyst-sda


Установить зависимости

pip install -r requirements.txt


Создать .env в корне проекта

Создайте файл: .env

И вставьте: OPENAI_API_KEY=ваш_api_ключ


Запустить приложение

streamlit run app.py


Демонстрация

Видео-демо (будет добавлено)

Используемые технологии:

Python 

Streamlit

OpenAI API

Python-dotenv

JSON / Markdown

Mermaid 


Особенности реализации:

безопасный парсинг JSON через safe_json_parse()

диалоговая сессия сохраняется через st.session_state

двухколоночный интерфейс

генерация BRD по строгой структуре

экспорт документа в .md


Авторы проекта:

Ongarbayeva Aigerim

Aitkazy Saida

Kossymzhanova Dana


## Скриншоты приложения

![Interface](screenshots/interface.png)

Это стартовый экран приложения: чат с агентом и область для отображения результатов.


![Dialog](screenshots/dialog.png)

Пример того, как AI-ассистент ведёт разговор, задаёт вопросы и уточняет требования.


![JSON](screenshots/json.png)

Структурированный JSON, который генерируется после завершения диалога.


![BRD](screenshots/brd.png)

Готовый Business Requirements Document, который формируется автоматически.


![Mermaid](screenshots/mermaid.png)

Автоматически построенная диаграмма бизнес-процесса.


