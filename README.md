# Проект Telegram Scraper


Для работы потребуется:

- **Poetry** — для управления зависимостями и виртуальными окружениями.
- **Docker** — для контейнеризации PostgreSQL и других компонентов, если это необходимо.
- **Python 3.12** (или версия, указанная в `pyproject.toml`).


## Запуск проекта

Создать .env по образу и подобию примера

## Локальный запуск на Unix системах

**Установка Poetry** через Python (рекомендуется):

   Для установки Poetry выполните следующую команду:

   ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    export PATH="$HOME/.local/bin:$PATH"
    ```

Проверить версию 
    poetry --version


Если версия poetry > 2, 
   ```bash
    poetry config virtualenvs.in-project true
    
    poetry config virtualenvs.prefer-active-python true
    
    poetry config virtualenvs.create true
    ```

   ```bash
   poetry install
   ```
   ```bash
   source .venv/bin/activate
   ```

Запустить БД:
    ```bash
    docker run --name tg_scrap -e POSTGRES_USER=tg_scrap -e POSTGRES_PASSWORD=tg_scrap -p 5432:5432 -d postgres:17-alpine
    ```

Запустить скрипт:
   ```bash
    poetry run python -m telegram_scraper.main
   ```


## Запуск в докер компоузе
**!!Для запуска требуется уже созданный файл сессии session_name.session который нужно положить возле докер компоуз файла!!**
   ```bash
    docker compose up
   ```

