# Bot personal expenses

Bot Personal Expenses is a Telegram bot that helps to keep track of personal expenses. It allows you to view your spending statistics for a month, taking into account the limits you set for certain categories. You can also change limits for categories, set or delete accounts to which your expenses will be tied.

All expenses are recorded in a database in dollars, taking into account the current exchange rate, and expenses are also recorded in a Google Spreadsheet (added for personal use).

## Technologies used

* Python 3.10
* Aiogram library for creating the Telegram bot
* SQLite database
* Requests and BeautifulSoup modules for web scraping to get the current exchange rate of currencies
* Google Sheets API for recording expenses

## How to run the project

Clone the repository and navigate to it in the command line:

```
git clone https://github.com/Evgenia789/bot_personal_expenses
cd bot_personal_expenses 
```

Create and activate a virtual environment:

```
python -m venv venv
source venv/Scripts/activate
```

In the project directory, create a `bot.ini` file and add the following:

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

where:

* `TELEGRAM_TOKEN` is the token obtained from BotFather
* `ID_1`, `ID_2`, etc. are the IDs of the users who are allowed to use the bot
* `expenses_table`, `incomes_table`, `currency_table`, `total_amount_table` are the names of the Google Sheets you will use for recording expenses (if you want to use this feature).

For using Google Sheets API, you need to follow the instructions on this page: [https://github.com/burnash/gspread/blob/master/docs/oauth2.rst](https://github.com/burnash/gspread/blob/master/docs/oauth2.rst)

## Author

Evgenia Pankova

## License

This project is under the MIT License - see the LICENSE file for details.
