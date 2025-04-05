# Telegram-shop-bot

## Описание
`Aiogram3` `PostgreSQL` `aiocryptopay` `asyncpg`
Telegram-shop-bot - это бот, предназначенный для создания простого магазина в Telegram. 

## Возможности

- Простое управление товарами
- Удобный интерфейс
- Автоматическое управление платежами

## Установка

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/Nethanter-del/Telegram-shop-bot
    ```
2. Установите зависимости:
    ```bash
    cd Telegram-shop-bot
    pip install -r requirements.txt
    ```
3. Отредактируйте `config.env`
4. Запустите бота:
    ```bash
    py main.py
    ```

## Использование

- Запустите бота
    ```bash
    py main.py
    ```
## Администрирование 
- /admins - список администраторов
- /grant_admin [id] - Добавить амиинистратора 
- /ungrant_admin [id] - Убрать администратора
- /add_money [id] [Сумма] - изменение баланса
- /create_product [Категория] [Название] [Описание] [Цена] [Товар] - создание товара
## Вклад

Приветствуются любые вклады!

## Лицензия

Этот проект лицензирован под лицензией MIT.
