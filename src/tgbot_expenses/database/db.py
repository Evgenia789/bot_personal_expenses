import sqlite3
from datetime import datetime
from typing import List, Tuple


class Database:
    __instance = None
    connection = None
    cursor = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Database, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self) -> None:
        self.connection = sqlite3.connect(
            "src/tgbot_expenses/database/finance.db"
        )
        self.cursor = self.connection.cursor()
        self.check_db_exists()

    def __call__(self, *args, **kwargs):
        self.__init__(*args, **kwargs)
        return self.cursor

    def _init_db(self):
        """Initializes the database"""
        with open("src/tgbot_personal_expenses/database/createdb.sql",
                  "r", encoding="utf-8") as f:
            sql = f.read()
        self.cursor.executescript(sql)
        self.connection.commit()

    def check_db_exists(self):
        """Checks if the database is initialized, if not, initializes"""
        self.cursor.execute("SELECT name FROM sqlite_master "
                            "WHERE type='table' AND name='item'")
        table_exists = self.cursor.fetchall()
        if table_exists:
            return
        self._init_db()

    def insert_item(self, category_name: str, bill_name: str, amount: int) -> None:
        """Insert a new entry"""
        category_id = self.fetchone("category", category_name)
        bill_id = self.fetchone("bill", bill_name)
        self.cursor.execute(f"INSERT INTO item VALUES ({amount}, {category_id}, {bill_id}, datetime('now','localtime'))")
        self.connection.commit()
    
    def get_category_limit(self, category_name: str) -> int:
        """Get category limit"""
        self.cursor.execute(f"SELECT limit_amount FROM category WHERE name='{category_name}'")
        result = self.cursor.fetchone()
        return result[0]
    
    def update_limit(self, category_name: str, new_limit: int) -> None:
        """Update category limit"""
        self.cursor.execute(f"UPDATE category SET limit_amount='{new_limit}' WHERE name='{category_name}'")
        self.connection.commit()
        return
    
    def archive_bill(self, bill_name: str) -> None:
        """Send the bill to the archive"""
        self.cursor.execute(f"UPDATE bill SET status='archive' WHERE name='{bill_name}'")
        self.connection.commit()
        return
    
    def get_all_bills(self) -> str:
        """Get all bills"""
        self.cursor.execute(f"SELECT name FROM bill WHERE status='active'")
        bills = self.cursor.fetchall()
        return  ";".join([bill[0] for bill in bills])
    
    def get_all_categories(self) -> str:
        """Get all categories"""
        self.cursor.execute(f"SELECT name FROM category")
        categories = self.cursor.fetchall()
        return ";".join([category[0] for category in categories])

    def insert_account(self, account_name: str) -> None:
        """Insert a new entry"""
        self.cursor.execute(f"INSERT INTO bill (name, status) VALUES ('{account_name}', 'active')")
        self.connection.commit()

    def fetchone(self, table: str, field_name: str):
        self.cursor.execute(f"SELECT id FROM {table} WHERE name='{field_name}'")
        result = self.cursor.fetchone()
        return result[0]

    def fetchall(self, table: str, columns: List[str]) -> List[Tuple]:
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
        # columns_joined = ", ".join(["total", "category_id", "month"])
        current_month = f"{datetime.now().month}-{datetime.now().year}"
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
            for index, column in enumerate(["category_name", "limit_expenses", "total", "month"]):
                dict_row[column] = row[index]
            result.append(dict_row)
        return result


database = Database()


# (f"SELECT IFNULL(SUM(amount), '0') AS total, category.name AS category_name, strftime('%m-%Y', date) AS cur_date, category.limit_amount AS limit_expenses FROM item RIGHT JOIN category ON item.category_id=category.id WHERE cur_date='{current_month}' GROUP BY category_id")