# Bot personal expenses

Bot personal expenses позволяет вести учет личных трат. Ты можешь просмотреть статистику своих трат за месяц с учетом установленных тобой лимитов на определенные категории. Также ты можешь изменять лимиты для категорий, задать или удалить счета к которым будут привязаны твои траты.

Все траты заносятся в базу данных с переводом в доллары с учетом актуального курса валют, и также траты заносятся в google таблицу (добавлено для личного пользования)

## Стек технологий

* проект написан на Python 3.10 с использованием библиотеки Aiogram
* база данных - Sqllite
* для получения актуального курса валют парсим данные из страницы поисковой выдачи Google с помощью модулей requests и BeautifulSoup

## Как запустить проект

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Evgenia789/bot_personal_expenses
cd bot_personal_expenses 
```

Создать и активировать виртуальное окружение:

```
python -m venv venv
source venv/Scripts/activate
```

В дериктории проекта создтье файл bot.ini , в котором необходимо прописать следующее :

```
[tg_bot]
TELEGRAM_TOKEN=""

[allowed_ids]
ID_1=""
ID_2=""

[google_tables]
expenses_table=your_table_name
incomes_table=your_table_name
currency_table=your_table_name
total_amount_table=your_table_name

```

где:

TELEGRAM_TOKEN - это токен телеграм полученный у BotFather
ID_1, ID_2 - это id пользователей которым разрешен доступ к боту   

Для занесения данных в гугл таблицу (если необходимо), нужно получить доступ к электронным таблицам через Google Sheets API. Это можно делать согласно: https://github.com/burnash/gspread/blob/master/docs/oauth2.rst

## Авторы

* Evgenia Pankova

## Лицензия

Этот проект находится под лицензией MIT License - подробности см. в файле LICENSE.
