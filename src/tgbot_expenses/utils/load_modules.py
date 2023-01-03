import os


def load_module(name: str, cur_dir: str):
    """Process of loading modules"""
    new_path = f"{cur_dir}\\tgbot_expenses\\{name}"
    res = {}
    # check subfolders
    lst = os.listdir(new_path)
    dir = []
    for d in lst:
        if d.startswith("_"):
            continue
        s = os.path.abspath(new_path) + os.sep + d
        if os.path.isdir(s) and os.path.exists(s + os.sep + "__init__.py"):
            dir.append(d)

    # load the modules
    for d in dir:
        res[d] = __import__(
            f"src.tgbot_expenses.{name}." + d, fromlist=["*"]
        )

    return res
