import os


def remove_extension(filename: str) -> str:
    """Удаляет расширение из имени файла.

    :param filename: Имя файла с расширением.
    :return: Имя файла без расширения.
    """
    return os.path.splitext(filename)[0]


def create_folder_if_not_exists(folder_path: str):
    """Создает папку, если она еще не существует.

    :param folder_path: Путь к папке.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def get_output_file_path(output_folder: str, filename: str) -> str:
    """Формирует полный путь к файлу в указанной папке.

    :param output_folder: Папка для сохранения файла.
    :param filename: Имя файла без расширения.
    :return: Полный путь к файлу.
    """
    return os.path.join(output_folder, f"output_{filename}.docx")
