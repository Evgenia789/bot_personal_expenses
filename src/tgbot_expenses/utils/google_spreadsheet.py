from typing import Any, List, Union

import gspread
from google.oauth2.service_account import Credentials


def get_spreadsheet() -> gspread.Spreadsheet:
    """
    Add new data to Google Spreadsheet

    :return: None
    """
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


def add_data_to_google_table(values: List[Union[int, str]],
                             title: str) -> None:
    """
    Add new data to the Google Spreadsheet with the specified title.

    :param values: A list of values for the new row. The first value can be an
                   integer index for the new row, or a string representing
                   a date or other identifier for the data.
    :type values: List[Union[int, str]]
    :param title: The title of the worksheet where the data will be added.
    :type title: str
    :return: None
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

    :param title: The title of the worksheet to update.
    :type title: str
    :param row: The row number to update.
    :type row: int
    :param column: The column number to update.
    :type column: int
    :param value: The value to insert at the specified row and column.
    :type value: Any
    :return: None
    """
    sh = get_spreadsheet()
    worksheet = sh.worksheet(title=title)
    worksheet.update_cell(row=row, col=column, value=value)

    return
