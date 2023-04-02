# Bot personal expenses

<p align="center">
    <img src="https://github.com/Evgenia789/bot_personal_expenses/blob/main/public/make_expenses.gif" alt="animated" align="left" />
    <img src="https://github.com/Evgenia789/bot_personal_expenses/blob/main/public/settings_category.gif" alt="animated" />
</p>

Bot Personal Expenses is a Telegram bot that helps to keep track of personal expenses. It allows you to view your spending statistics for a month, taking into account the limits you set for certain categories. You can also change the limits for categories, set or delete accounts to which your expenses will be linked, create or delete a category, view current exchange rates and convert funds from one account to another.

## Technologies used

* Python 3.10
* Aiogram library for creating the Telegram bot
* PostgreSQL database
* Requests and BeautifulSoup modules for web scraping to get the current exchange rate of currencies

## How to run the project

Clone the repository and navigate to it in the command line:

```bash
git clone https://github.com/Evgenia789/bot_personal_expenses
cd bot_personal_expenses 
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/Scripts/activate
```

In the project directory, create a `bot.ini` file and add the following:

```ini
[tg_bot]
TELEGRAM_TOKEN=""

[allowed_ids]
ID_1=""
ID_2=""

[postgres_database]
POSTGRES_HOST=""
POSTGRES_PORT=""
POSTGRES_USER=""
POSTGRES_PASSWORD=""
POSTGRES_DB=""

```

where:

* `TELEGRAM_TOKEN` is the token obtained from BotFather
* `ID_1`, `ID_2`, etc. are the IDs of the users who are allowed to use the bot
* `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_USER`,
  `POSTGRES_PASSWORD,` `POSTGRES_DB` are variables to connect to the PostgreSQL database.

## Author

Evgenia Pankova

## License

Licensed under the [MIT](https://github.com/microsoft/vscode/blob/main/LICENSE.txt) license.
