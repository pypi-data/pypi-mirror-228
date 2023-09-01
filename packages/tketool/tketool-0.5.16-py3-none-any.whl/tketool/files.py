import os, importlib.util


def create_folder_if_not_exists(*args) -> str:
    """
    Create a folder at the specified path if it doesn't exist.

    :param args: Segments of the path, similar to os.path.join.
    :return: The constructed path.
    """
    path = os.path.join(*args)
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    return path


def write_file(path: str, lines: list) -> None:
    """
    Write a list of lines to a file.

    :param path: Path to the file.
    :param lines: List of lines to write.
    """
    try:
        with open(path, 'w') as ff:
            ff.write("\n".join(lines))
    except Exception as e:
        print(f"Error writing to file {path}. Reason: {e}")


def read_file(path: str) -> list:
    """
    Read lines from a file.

    :param path: Path to the file.
    :return: List of lines from the file.
    """
    try:
        with open(path, 'r') as ff:
            return [line.strip() for line in ff.readlines()]
    except Exception as e:
        print(f"Error reading from file {path}. Reason: {e}")
        return []


def list_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            yield root, file
