from app.data_extractor import process_html_folder
from app.data_processor import transform_table
from app.docx_writer import write_to_docx
from app.utils import (
    remove_extension,
    create_folder_if_not_exists,
    get_output_file_path,
)


def main():
    """Основная функция для обработки HTML-файлов, трансформации данных таблиц
    и записи результатов в DOCX файлы.

    Шаги выполнения:
    1. Создание выходной папки, если она не существует.
    2. Обработка папки с HTML-файлами и извлечение данных таблиц.
    3. Трансформация данных таблиц с учетом коэффициентов.
    4. Запись трансформированных таблиц в DOCX файлы.
    """
    folder_path = "parse_data"
    output_folder = "output_data"

    create_folder_if_not_exists(output_folder)

    table_data_all = process_html_folder(folder_path)

    for filename, (tables, coefficients) in table_data_all.items():
        filename = remove_extension(filename)
        transformed_tables = []

        for _, table_data in enumerate(tables):
            transformed_table, colored_cells = transform_table(
                table_data, coefficients
            )
            transformed_tables.append((transformed_table, colored_cells))

        docx_filename = get_output_file_path(output_folder, filename)
        write_to_docx(
            docx_filename, {filename: (transformed_tables, coefficients)}
        )


if __name__ == "__main__":
    main()
