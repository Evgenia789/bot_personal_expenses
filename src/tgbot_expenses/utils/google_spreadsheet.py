import gspread
from google.oauth2.service_account import Credentials


def add_data_to_google_table(data: list, name_title: str) -> None:
    """Add new data to Google Spreadsheet"""
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    # You can download the service_account.json file when you access
    # the spreadsheets via the Google Sheets API. You can do it
    # by https://github.com/burnash/gspread/blob/master/docs/oauth2.rst
    credentials = Credentials.from_service_account_file(
        'src/tgbot_expenses/database/service_account.json',
        scopes=scopes
    )

    gc = gspread.authorize(credentials)

    sh = gc.open("Expenses")  # You need to specify the name of your table

    worksheet = sh.worksheet(title=name_title)

    worksheet.insert_row(data, data[0]+1)
