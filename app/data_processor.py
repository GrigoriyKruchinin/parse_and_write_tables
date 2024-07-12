from typing import List

from app.data_extractor import TableData


def create_header(table_data: TableData, coefficients: List[int]) -> List[str]:
    """Создает заголовок таблицы на основе исходных данных и
    коэффициентов.

    :param table_data: Объект TableData, представляющий исходную таблицу.
    :param coefficients: Список целых чисел, представляющий коэффициенты
        для добавления в заголовок.
    :return: Список строк, представляющий заголовок таблицы.
    """
    header = (
        ["C", "-"]
        + [str(coef) for coef in coefficients]
        + ["0"] * (len(table_data.header) - len(coefficients) - 2)
    )
    return header


def create_variable_header(table_data: TableData) -> List[str]:
    """Создает переменный заголовок таблицы B, A0, A1, A2 и т.д.

    :param table_data: Объект TableData, представляющий исходную таблицу.
    :return: Список строк, представляющий переменный заголовок таблицы.
    """
    variable_header = ["B", "A0"] + [
        f"A{i}" for i in range(1, len(table_data.header) - 1)
    ]
    return variable_header


def insert_first_element(row: List[str], coefficients: List[int]) -> None:
    """Вставляет первый элемент в строку в соответствии с условиями.

    :param row: Строка таблицы, в которую нужно вставить первый элемент.
    :param coefficients: Список целых чисел, представляющий коэффициенты
        для добавления в заголовок.
    """
    if not row[0].startswith("x"):
        row.insert(0, "")
    elif row[0].startswith("x"):
        var_index = int(row[0][1:])
        if var_index <= len(coefficients):
            row.insert(0, str(coefficients[var_index - 1]))
        else:
            row.insert(0, "0")


def update_colored_cells_if_match(table_data: TableData) -> None:
    """Обновляет список цветовых ячеек в объекте TableData на основе
    текущих данных таблицы.

    Проверяет каждый объект цветовой ячейки из table_data.colored_cells и
    ищет соответствующие значения в table_data.rows. Если найдено
    совпадение, обновляет список colored_cells.

    :param table_data: Объект TableData, представляющий данные таблицы.
    """
    color_objs = table_data.get_colored_cells()
    for color_obj in color_objs:
        # Не учитываем первые два столбца и две первых строки
        for i in range(2, len(table_data.rows)):
            for j in range(2, len(table_data.rows[i])):
                if table_data.rows[i][j] == color_obj[0]:
                    # Перезаписываем инфо о цветной ячейке, учитывая
                    # две строки header и первый вставленный столбец
                    table_data.update_colored_cells(
                        (
                            table_data.rows[i][j],
                            i + 2,
                            j + 1,
                        )
                    )
                    return


def transform_table(
    table_data: TableData, coefficients: List[int]
) -> List[List[str]]:
    """Преобразует данные таблицы с учетом коэффициентов и создает новую
    таблицу с заголовком.

    :param table_data: Объект TableData, представляющий исходную таблицу.
    :param coefficients: Список целых чисел, представляющий коэффициенты
        для добавления в заголовок.
    :return: Список списков строк (List[List[str]]), представляющий
        преобразованную таблицу с заголовком.
    """
    update_colored_cells_if_match(table_data)
    header = create_header(table_data, coefficients)
    variable_header = create_variable_header(table_data)
    transformed_rows = [variable_header] + table_data.rows
    transformed_table = [header] + transformed_rows

    for row in transformed_table:
        insert_first_element(row, coefficients)

    transformed_table = [
        [str(cell) for cell in row] for row in transformed_table
    ]

    return transformed_table, table_data.get_colored_cells()
