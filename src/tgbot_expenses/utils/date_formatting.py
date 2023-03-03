from datetime import datetime

import pytz


def get_now_date(date_format: str = "%d/%m/%y", timezone: str = "UTC") -> str:
    """Get the current date and time as a formatted string.

    :param date_format: A string that specifies the format of the date.
                        The default format is "%d/%m/%y".
    :type date_format: str
    :param timezone: A string that specifies the timezone to use. The default
                     timezone is "UTC".
    :type timezone: str
    :return: str
    """
    date_today = datetime.now(pytz.timezone(timezone))

    return date_today.strftime(date_format)
