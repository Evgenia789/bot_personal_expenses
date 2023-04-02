from datetime import datetime
from typing import List, Tuple

import matplotlib.pyplot as plt


async def get_chart(data: List[Tuple]) -> str:
    """
    Generate and save a pie chart of expenses for the current month.

    :param data: A list of tuples containing monthly expense data.
                 Each tuple should have the following format:
                 (category_name: str, total: Decimal).
    :type data: List[Tuple]
    :return: str
    """
    path_to_chart = "src/tgbot_expenses/utils/chart/output.png"
    categories = []
    amount = []

    for d in data:
        if d["total"] != 0:
            categories.append(d["category_name"])
            amount.append(d["total"])
    fig1, ax1 = plt.subplots()
    ax1.pie(amount, labels=categories, autopct='%1.0f%%')
    ax1.axis('equal')
    ax1.set_title(label=f"Expenses for {datetime.now().strftime('%B')}",
                  fontweight="bold", pad=20)
    plt.savefig(path_to_chart)
    return path_to_chart
