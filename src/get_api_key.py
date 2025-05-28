def read_file(file_path: str) -> str:
    """
    Reads the first line from a text file.

    Args:
        file_path (str): The path to the text file.

    Returns:
        str: The first line of the file as a string.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.readline().strip()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""
