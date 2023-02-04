from dataclasses import dataclass


@dataclass
class ButtonText:
    main_menu = "View statistics;Make expenses;Make income;Settings"
    confirmation = "Confirm;Cancel"


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
    bills = "Do you want to add or delete?"
    new_bill = "Send the bill name"
    archive_bill = "Choose the bill you want to delete"
    result_archive = "The bill archived"
    warning_number = "You need to enter a number!"
    start = "You are in the process of entering expenses"
