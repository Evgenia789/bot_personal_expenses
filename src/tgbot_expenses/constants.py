from dataclasses import dataclass


@dataclass
class QuestionText:
    """
    A dataclass representing the text of a questions.
    """
    main_menu = "What do you want to do?"
    category = "Choose a category where your expenses belong"
    bill = "Choose the bill"
    amount = "Enter the amount"
    confirmation = ("Confirm the entered data or click the "
                    "'Cancel' button to start over")
    last_message = "Data added!"
    limits = "Choose category to change the limit"
    changing = "Do you want to add or delete?"
    new_bill = ("Send the bill name for example: "
                "Bill Name USD")
    new_category = "Send the category name"
    category_limit = "Send a limit for a new category"
    archive_bill = "Choose the bill you want to delete"
    archive_category = "Choose the category you want to delete"
    result_archive = "Archived"
    warning_number = "You need to enter a number!"
    start = "You are in the process of entering expenses"
    from_bill = "Select the bill you want to transfer money from"
    to_bill = "Select the bill to which you want to transfer money"
