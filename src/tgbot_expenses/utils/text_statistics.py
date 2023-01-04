from typing import List, Tuple


async def get_data(data: List[Tuple]) -> str:
    """Get data for statistics"""
    print(data)
    text_msg = "\n"
    total_amount = 0
    total_limit = 0
    for d in data:
        emoji = "😱" if d['total'] >= d['limit_expenses'] else ""
        text_msg = text_msg + (f"\n<b>{d['category_name']}:</b> {emoji}"
                               f"{d['total']} / {d['limit_expenses']}")
        total_amount += d['total']
        total_limit += d['limit_expenses']
    text_msg = text_msg + (f"\n\n<b>Total expenses:</b>"
                           f" {total_amount} / {total_limit}")
    return text_msg
