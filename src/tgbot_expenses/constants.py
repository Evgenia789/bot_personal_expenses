from dataclasses import dataclass


@dataclass(frozen=True)
class QuestionText:
    """
    A dataclass representing the text of a questions.
    """
    main_menu = "What do you want to do?"
    category = "Choose a category where your expenses belong"
    account = "Choose the account"
    amount = "Enter the amount"
    confirmation = ("Confirm the entered data or click the "
                    "'Cancel' button to start over")
    last_message = "Data added!"
    limits = "Choose category to change the limit"
    changing = "Do you want to add or delete?"
    new_account = ("Send the account name for example: "
                   "Account Name USD")
    new_category = "Send the category name"
    category_limit = "Send a limit for a new category"
    archive_account = "Choose the account you want to delete"
    archive_category = "Choose the category you want to delete"
    result_archive = "Archived"
    warning_number = "You need to enter a number!"
    start = "You are in the process of entering expenses"
    from_account = "Select the account you want to transfer money from"
    to_account = "Select the account to which you want to transfer money"
    empty_data = ("The required categories or accounts have not been created."
                  "\nYou need to add them via `Settings`-> `Change account`/"
                  "`Change Category`/ -> `Add Account`/`Add Category`.")
    initialization = ("You should press the /init command "
                      "to start using the bot")
