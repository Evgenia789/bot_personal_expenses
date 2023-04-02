from typing import List, Tuple


async def get_data(data: List[Tuple]) -> str:
    """
    Generate a formatted string with the data for the monthly expenses
    statistics.

    :param data: A list of tuples containing the category name,
                 the total expense and the expense limit.
    :type data: List[Tuple[str, Decimal, Decimal]]
    :return: str
    """
    text_msg = "\n"
    total_amount = 0
    total_limit = 0
    for d in data:
        emoji = "😱" if d['total'] >= d['limit_expenses'] else ""
        text_msg = text_msg + (f"\n<b>{d['category_name']}:</b> {emoji}"
                               f"{round(d['total'], 2)} / "
                               f"{d['limit_expenses']}")
        total_amount += d['total']
        total_limit += d['limit_expenses']
    text_msg = text_msg + (f"\n\n<b>Total expenses:</b>"
                           f" {round(total_amount, 2)} / {total_limit}")
    return text_msg
