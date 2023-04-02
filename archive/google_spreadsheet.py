from typing import Any, List, Union

from google.oauth2.service_account import Credentials
from gspread_asyncio import (AsyncioGspreadClientManager,
                             AsyncioGspreadSpreadsheet)

from src.tgbot_expenses.config import load_config


def get_credentials() -> Credentials:
    """
    Returns Google API credentials required to access a Google Sheets API.

    This function reads the service account file 'service_account.json' in the
    specified directory, and returns a `Credentials` object with the necessary
    authorization information to access the Google Sheets API.

    :return: A `Credentials` object with authorization information.
    """
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    # You can download the service_account.json file when you access
    # the spreadsheets via the Google Sheets API. You can do it
    # by https://github.com/burnash/gspread/blob/master/docs/oauth2.rst
    credentials = Credentials.from_service_account_file(
        filename='src/tgbot_expenses/database/service_account.json'
    )
    scoped = credentials.with_scopes(scopes=scopes)

    return scoped


def create_agcm_object() -> AsyncioGspreadClientManager:
    """
    Creates an `AsyncioGspreadClientManager` object which provides access to
    the Google Sheets API using asynchronous calls.

    :return: An `AsyncioGspreadClientManager` object.
    """
    credentials = get_credentials
    agcm = AsyncioGspreadClientManager(credentials_fn=credentials)

    return agcm


async def get_spreadsheet() -> AsyncioGspreadSpreadsheet:
    """
    Returns an AsyncioSpreadsheet object for the specified Google Sheet.

    :param title: The title of the Google Sheet to open.
    :return: An AsyncioSpreadsheet object.
    """
    agcm = create_agcm_object()
    agc = await agcm.authorize()

    config = load_config("bot.ini")
    title = config.googletables.spreadsheet

    sh = await agc.open(title=title)

    return sh


async def add_data_to_google_table(values: List[Union[int, str]],
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
    sh = await get_spreadsheet()
    worksheet = await sh.worksheet(title=title)
    if isinstance(values[0], int):
        await worksheet.insert_row(values=values, index=values[0]+1)
    else:
        await worksheet.append_row(values=values)


async def update_data_to_google_table(title: str, row: int,
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
    sh = await get_spreadsheet()
    worksheet = await sh.worksheet(title=title)
    await worksheet.update_cell(row=row, col=column, value=value)
