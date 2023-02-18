import os


def load_module(name: str, cur_dir: str):
    """Process of loading modules"""
    new_path = f"{cur_dir}\\tgbot_expenses\\{name}"

    for root, dirs, files in os.walk(new_path):
        for file in files:
            if file.endswith('.py') and not file.startswith('_'):
                path_root = ".".join(root.split('\\')[3:])
                __import__(path_root + "." + file.split(".")[0], fromlist=())

    return
