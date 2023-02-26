from typing import Any

import gspread
from google.oauth2.service_account import Credentials


def get_spreadsheet() -> gspread.Spreadsheet:
    """Add new data to Google Spreadsheet"""
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    # You can download the service_account.json file when you access
    # the spreadsheets via the Google Sheets API. You can do it
    # by https://github.com/burnash/gspread/blob/master/docs/oauth2.rst
    credentials = Credentials.from_service_account_file(
        filename='src/tgbot_expenses/database/service_account.json',
        scopes=scopes
    )

    gc = gspread.authorize(credentials=credentials)
    # You need to specify the name of your table
    sh = gc.open(title="Expenses")

    return sh


def add_data_to_google_table(values: list, title: str) -> None:
    """
    Add new data to Google Spreadsheet

    :param list values: List of values for the new row.
    """
    sh = get_spreadsheet()
    worksheet = sh.worksheet(title=title)
    if isinstance(values[0], int):
        worksheet.insert_row(values=values, index=values[0]+1)
    else:
        worksheet.append_row(values=values)

    return


def update_data_to_google_table(title: str, row: int,
                                column: int, value: Any) -> None:
    """
    Update the data for the specified column in the Google Spreadsheet
    """
    sh = get_spreadsheet()
    worksheet = sh.worksheet(title=title)
    worksheet.update_cell(row=row, col=column, value=value)

    return
