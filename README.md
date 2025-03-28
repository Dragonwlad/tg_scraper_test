# Проект Telegram Scraper


Для работы потребуется:

- **Poetry** — для управления зависимостями и виртуальными окружениями.
- **Docker** — для контейнеризации PostgreSQL и других компонентов, если это необходимо.
- **Python 3.12** (версия, указанная в `pyproject.toml`).


## Запуск проекта

Создать .env по образу и подобию примера. 
Если планируется локальный запуск, в DB_HOST указать **localhost**, если в контейнере **db**

## Локальный запуск на Unix системах
Установка python

    sudo apt install python3.12

**Установка Poetry** через Python:

    curl -sSL https://install.python-poetry.org | python3 -

    export PATH="$HOME/.local/bin:$PATH"

Проверить версию, проект на 2.1.1, рекомендуется версия > 2

    poetry --version

Если poetry впервые установлен и версия > 2:

    poetry config virtualenvs.in-project true
    
    poetry config virtualenvs.prefer-active-python true
    
    poetry config virtualenvs.create true

Установка зависимостей

    poetry install

Запуск окружения

    source .venv/bin/activate

Запустить БД в контейнере:

    docker run --name tg_scrap -e POSTGRES_USER=tg_scrap -e POSTGRES_PASSWORD=tg_scrap -p 5432:5432 -d postgres:15-alpine

Запустить скрипт:

    poetry run python -m telegram_scraper.main

На указанный номер в ТГ придет код подтверждения, ввести его в консоль.


## Запуск через docker compose 
**!! Для запуска требуется разместить уже созданный файл сессии session_name.session рядом с docker-compose.yml**
Для создания файла сессии требуется запустить скрипт локально, по инструкции выше
    
В telegram_scraper выполнить
    
    docker compose up


## Проверка
Эндпоинт для получения данных не реализован. Проверить наполнение БД можно подключившись напрямую.