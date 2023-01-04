import gspread
from google.oauth2.service_account import Credentials


def add_data_to_google_table(data: list) -> None:
    """Add new data to Google Spreadsheet"""
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    credentials = Credentials.from_service_account_file(
        'src/tgbot_expenses/database/service_account.json',
        scopes=scopes
    )

    gc = gspread.authorize(credentials)

    sh = gc.open("Expenses")

    worksheet = sh.sheet1

    worksheet.insert_row(data, data[0]+1)
