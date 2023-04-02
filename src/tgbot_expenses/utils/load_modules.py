import os
import asyncio


async def load_module(name: str, cur_dir: str) -> None:
    """
    Walks through the directory at the specified path and imports
    any Python modules (i.e. files ending in `.py`) that are not
    marked with an underscore at the beginning of their filename. The imported
    modules are added to the local namespace.

    :param name: Name of the directory containing the modules to load.
    :type name: str
    :param cur_dir: Current working directory where the `name` directory
                    is located.
    :type name: str
    :return: None
    :raises ImportError: If a module cannot be imported due to errors in
                         the code.
    """
    new_path = f"{cur_dir}\\tgbot_expenses\\{name}"
    # new_path = os.path.abspath("src")
    for root, dirs, files in os.walk(new_path):
        for file in files:
            if file.endswith('.py') and not file.startswith('_'):
                path_root = ".".join(root.split('\\')[3:])
                await asyncio.to_thread(
                    __import__, path_root + "." + file.split(".")[0], fromlist=()
                )
