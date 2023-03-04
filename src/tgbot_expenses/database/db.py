import sqlite3
from typing import List, Tuple

from src.tgbot_expenses.config import load_config
from src.tgbot_expenses.utils.date_formatting import get_now_date
from src.tgbot_expenses.utils.google_spreadsheet import (
    add_data_to_google_table, update_data_to_google_table)


class Database:
    """
    Singleton class that handles database connections and initialization.
    """
    __instance = None
    connection = None
    cursor = None
    config = load_config("bot.ini")

    def __new__(cls, *args, **kwargs):
        """
        Create a singleton instance of the Database class.

        :return: A singleton instance of the Database class.
        """
        if cls.__instance is None:
            cls.__instance = super(Database, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self) -> None:
        """
        Initialize a connection to the SQLite database and create it
        if it doesn't exist.

        :return: None
        """
        self.connection = sqlite3.connect(
            "src/tgbot_expenses/database/finance.db"
        )
        self.cursor = self.connection.cursor()
        self.check_db_exists()

    def __call__(self, *args, **kwargs):
        """
        Return the database cursor object.

        :param args: Arguments to be passed to the __init__ method.
        :param kwargs: Keyword arguments to be passed to the __init__ method.
        :return: Cursor object for the database connection.
        """
        self.__init__(*args, **kwargs)
        return self.cursor

    def _init_db(self):
        """
        Initializes the SQLite database by executing the SQL commands
        in createdb.sql.
        """
        with open("src/tgbot_expenses/database/createdb.sql",
                  "r", encoding="utf-8") as f:
            sql = f.read()
        self.cursor.executescript(sql)
        self.connection.commit()

    def check_db_exists(self):
        """Checks if the database is initialized, if not, initializes"""
        self.cursor.execute("SELECT name "
                            "FROM sqlite_master "
                            "WHERE type='table' AND name='item'")
        table_exists = self.cursor.fetchall()
        if table_exists:
            return
        self._init_db()

    async def insert_item(self, category_name: str,
                          bill_name: str, amount: float, initial_amount: float) -> None:
        """
        Insert a new financial transaction into the database.

        :param category_name: The name of the category of the transaction.
        :type category_name: str
        :param bill_name: The name of the bill from which the transaction
                          is made.
        :type bill_name: str
        :param amount: The amount of the transaction.
        :type amount: float
        :param initial_amount: The initial amount of the bill before
                               the transaction.
        :type initial_amount: float
        """
        category_id = self.fetchone("category", category_name)
        bill_id = self.fetchone("bill", bill_name)
        self.cursor.execute(f"INSERT INTO "
                            "item (amount, category_id, bill_id, date) "
                            f"VALUES ({amount}, {category_id}, {bill_id}, "
                            "datetime('now','localtime'))")
        self.cursor.execute(f"UPDATE bill "
                            f"SET amount=amount-'{initial_amount}' "
                            f"WHERE id='{bill_id}'")
        self.connection.commit()

        # this code will be used before creating the main application to better
        # display expenses in GoogleSheets
        last_id = self.get_id_last_entry(table="item")
        await add_data_to_google_table(
            values=[last_id[0], amount, category_name, bill_name,
                    get_now_date(), initial_amount],
            title=self.config.googletables.expenses
        )
        last_amount = self.get_amount(bill_id=bill_id)[0]
        await update_data_to_google_table(
            title=self.config.googletables.total_amount, row=bill_id,
            column=3, value=float(last_amount))

    async def insert_income(self, bill_name: str, amount: float) -> None:
        """
        Inserts a new income entry into the database for a given bill.

        :param bill_name: The name of the bill for which to insert the income.
        :type bill_name: str
        :param amount: The amount of the income to insert.
        :type amount: float
        :return: None
        """
        bill_id = self.fetchone("bill", bill_name)
        self.cursor.execute(f"INSERT INTO "
                            "income (amount, bill_id, date) "
                            f"VALUES ({amount}, {bill_id}, "
                            "datetime('now','localtime'))")
        self.cursor.execute(f"UPDATE bill "
                            f"SET amount=amount+'{amount}' "
                            f"WHERE id='{bill_id}'")
        self.connection.commit()

        # this code will be used before creating the main application to better
        # display expenses in GoogleSheets
        last_id = self.get_id_last_entry(table="income")
        await add_data_to_google_table(
            values=[last_id[0], amount, bill_name, get_now_date()],
            title=self.config.googletables.incomes
        )
        last_amount = self.get_amount(bill_id=bill_id)[0]
        await update_data_to_google_table(
            title=self.config.googletables.total_amount, row=bill_id,
            column=3, value=float(last_amount))

    async def insert_account(self, account_name: str, account_amount: float) -> None:
        """
        Insert a new entry into the 'bill' table with the given account name
        and amount.

        :param account_name: The name of the account to insert.
        :type account_name: str
        :param account_amount: The amount associated with the account
                               to insert.
        :type account_amount: float
        :return: None
        """
        self.cursor.execute("INSERT INTO bill (name, amount, status) "
                            f"VALUES ('{account_name}', '{account_amount}', 'active')")
        self.connection.commit()

        # this code will be used before creating the main application to better
        # display expenses in GoogleSheets
        await add_data_to_google_table(
            values=[account_name, account_amount],
            title=self.config.googletables.total_amount
        )

    def insert_category(self, category_name: str, limit_amount: int) -> None:
        """
        Insert a new category entry into the 'category' table with the given name and limit amount.

        :param category_name: The name of the category to insert.
        :type category_name: str
        :param limit_amount: The limit amount for the category to insert.
        :type limit_amount: int
        :return: None
        """
        self.cursor.execute("INSERT INTO category (name, limit_amount, status) "
                            f"VALUES ('{category_name}', '{limit_amount}', 'active')")
        self.connection.commit()

    def get_category_limit(self, category_name: str) -> int:
        """
        Retrieve the limit amount for the given category from
        the 'category' table.

        :param category_name: The name of the category to retrieve
                              the limit amount for.
        :type category_name: str
        :return: The limit amount for the category.
        """
        self.cursor.execute(f"SELECT limit_amount "
                            "FROM category "
                            f"WHERE name='{category_name}'")

        return self.cursor.fetchone()[0]

    def get_id_last_entry(self, table: str) -> int:
        """
        Retrieve the id of the last entry in the given table.

        :param table: The name of the table to retrieve the id from.
        :type table: str
        :return: The id of the last entry in the table.
        """
        self.cursor.execute(f"SELECT max(id) FROM '{table}'")
        return self.cursor.fetchall()[0]

    def get_amount(self, bill_id: int) -> float:
        """
        Retrieve the amount associated with the given bill ID from
        the 'bill' table.

        :param bill_id: The ID of the bill to retrieve the amount for.
        :type bill_id: int
        :return: The amount associated with the bill.
        """
        self.cursor.execute(f"SELECT amount FROM bill WHERE id='{bill_id}'")
        return self.cursor.fetchall()[0]

    def get_all_bills(self) -> str:
        """
        Retrieve the names of all active bills from the 'bill' table.

        :return: A string containing the names of all active bills,
                 separated by semicolons.
        """
        self.cursor.execute("SELECT name FROM bill WHERE status='active'")
        bills = self.cursor.fetchall()

        return ";".join([bill[0] for bill in bills])

    def get_all_categories(self) -> str:
        """
        Retrieve the names of all categories from the 'category' table.

        :return: A string containing the names of all categories,
                 separated by semicolons.
        """
        self.cursor.execute("SELECT name FROM category WHERE status='active'")
        categories = self.cursor.fetchall()

        return ";".join([category[0] for category in categories])

    def update_limit(self, category_name: str, new_limit: int) -> None:
        """
        Update the limit amount for the given category in the 'category' table.

        :param category_name: The name of the category to update.
        :type category_name: str
        :param new_limit: The new limit amount to set for the category.
        :type new_limit: int
        :return: None
        """
        self.cursor.execute(f"UPDATE category "
                            f"SET limit_amount='{new_limit}' "
                            f"WHERE name='{category_name}'")
        self.connection.commit()

        return

    async def update_amount(self, bill_from: str, amount_old_currency: float,
                            currency_amount: float, bill_to: str) -> None:
        """
        Update the amount for the specified bills in the 'bill' table.

        :param bill_from: The name of the bill to subtract the old amount from.
        :type bill_from: str
        :param amount_old_currency: The old amount in the original currency to
                                    subtract from the 'bill_from'.
        :type amount_old_currency: float
        :param currency_amount: The amount in the new currency to add
                                to the 'bill_to'.
        :type currency_amount: float
        :param bill_to: The name of the bill to add the new amount to.
        :type bill_to: str
        :return: None
        """
        self.cursor.execute(f"UPDATE bill "
                            f"SET amount=amount-'{amount_old_currency}' "
                            f"WHERE name='{bill_from}'")
        self.cursor.execute(f"UPDATE bill "
                            f"SET amount=amount+'{currency_amount}' "
                            f"WHERE name='{bill_to}'")
        self.connection.commit()

        # this code will be used before creating the main application to better
        # display expenses in GoogleSheets
        await add_data_to_google_table(
            values=[bill_from, amount_old_currency, bill_to,
                    currency_amount, get_now_date(),
                    round(currency_amount/amount_old_currency, 4)],
            title=self.config.googletables.currency
        )
        id = self.fetchone(table="bill", field_name=bill_from)
        last_amount = self.get_amount(bill_id=id)[0]
        await update_data_to_google_table(
            title=self.config.googletables.total_amount, row=id,
            column=3, value=float(last_amount)
        )
        id = self.fetchone(table="bill", field_name=bill_to)
        last_amount = self.get_amount(bill_id=id)[0]
        await update_data_to_google_table(
            title=self.config.googletables.total_amount, row=id,
            column=3, value=float(last_amount)
        )

        return

    def archive_bill(self, bill_name: str) -> None:
        """
        Update the status of the specified bill to 'archive'
        in the 'bill' table.

        :param bill_name: The name of the bill to be archived.
        :type bill_name: str
        :return: None
        """
        self.cursor.execute(f"UPDATE bill "
                            "SET status='archive' "
                            f"WHERE name='{bill_name}'")
        self.connection.commit()

        return

    def archive_category(self, category_name: str) -> None:
        """
        Update the status of the specified category to 'archive'
        in the 'category' table.

        :param category_name: The name of the category to be archived.
        :type category_name: str
        :return: None
        """
        self.cursor.execute(f"UPDATE category "
                            "SET status='archive' "
                            f"WHERE name='{category_name}'")
        self.connection.commit()

        return

    def fetchone(self, table: str, field_name: str):
        """
        Retrieve the ID associated with the given field name
        from the specified table.

        :param table: The name of the table to retrieve the ID from.
        :type table: str
        :param field_name: The name of the field to retrieve the ID for.
        :type field_name: str
        :return: The ID associated with the field name.
        """
        self.cursor.execute(f"SELECT id FROM {table} WHERE name='{field_name}'")

        return self.cursor.fetchone()[0]

    def fetchall(self, table: str, columns: List[str]) -> List[Tuple]:
        """
        Retrieve all rows and columns from the specified table in the database.

        :param table: The name of the table to retrieve data from.
        :type table: str
        :param columns: The list of column names to retrieve data for.
        :type columns: List[str]
        :return: A list of tuples containing the data for each row and column.
        """
        columns_joined = ", ".join(columns)
        self.cursor.execute(f"SELECT {columns_joined} FROM {table}")
        rows = self.cursor.fetchall()
        result = []
        for row in rows:
            dict_row = {}
            for index, column in enumerate(columns):
                dict_row[column] = row[index]
            result.append(dict_row)
        return result

    def fetchallmonth(self) -> List[Tuple]:
        """
        Retrieve all the data for the current month
        from the 'item' and 'category' tables.

        :return: A list of dictionaries containing the category name,
                 limit amount, total expenses for the month,
                 and the current month.
        """
        current_month = f"{get_now_date(date_format='%m')}-{get_now_date(date_format='%Y')}"
        self.cursor.execute(f"SELECT name AS category_name, limit_amount, COALESCE(month_exp.total, 0) AS total, COALESCE(month_exp.cur_date, '{current_month}') AS month "
                            "FROM category "
                            "LEFT JOIN "
                            "(SELECT SUM(amount) AS total, category.name AS category_name, strftime('%m-%Y', date) AS cur_date, category.limit_amount AS limit_expenses "
                            "FROM item "
                            "LEFT JOIN category ON item.category_id=category.id "
                            f"WHERE cur_date='{current_month}' GROUP BY category_id) month_exp "
                            "ON month_exp.category_name=category.name")
        rows = self.cursor.fetchall()
        result = []
        for row in rows:
            dict_row = {}
            for index, column in enumerate(["category_name", "limit_expenses",
                                           "total", "month"]):
                dict_row[column] = row[index]
            result.append(dict_row)
        return result


database = Database()
