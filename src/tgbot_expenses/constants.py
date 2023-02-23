from dataclasses import dataclass


@dataclass
class QuestionText:
    main_menu = "What do you want to do?"
    category = "Choose a category where your expenses belong"
    bill = "Choose the bill"
    amount = "Enter the amount"
    confirmation = ("Confirm the entered data or click the "
                    "'Cancel' button to start over")
    last_message = "Data added!"
    limits = "Choose category to change the limit"
    changing = "Do you want to add or delete?"
    new_bill = ("Send the bill name in the format "
                "`<bill name> <currency name: RUB, RSD, EUR, LAR, USD>`")
    new_category = "Send the category name"
    category_limit = "Send a limit for a new category"
    archive_bill = "Choose the bill you want to delete"
    archive_category = "Choose the category you want to delete"
    result_archive = "Archived"
    warning_number = "You need to enter a number!"
    start = "You are in the process of entering expenses"
