import os
import re
from typing import List, Tuple, Dict

from bs4 import BeautifulSoup


class TableData:
    """Класс для представления данных таблицы."""

    def __init__(self, header, rows):
        """Инициализирует объект TableData с заголовком и строками
        таблицы.

        :param header: Список заголовков столбцов таблицы.
        :param rows: Список списков, представляющих строки таблицы.
        :param colored_cells: Cписок кортежей (value, row_index,
            col_index) для цветовых ячеек
        """
        self.header = header
        self.rows = rows
        self.colored_cells: List[Tuple[str, int, int]] = []

    def get_colored_cells(self):
        """Возвращает список кортежей (value, row_index, col_index) для
        цветовых ячеек.

        :return: Список кортежей (value, row_index, col_index) для
            цветовых ячеек.
        """
        return self.colored_cells

    def update_colored_cells(self, new_colored_cells):
        """Обновляет список colored_cells.

        :param new_colored_cells: Новый список значений закрашенных ячеек
            (без индексов).
        """
        self.colored_cells = new_colored_cells


def extract_coefficients_from_soup(soup: BeautifulSoup) -> List[int]:
    """Извлекает коэффициенты из HTML-разметки, представленной объектом
    BeautifulSoup.

    :param soup: Объект BeautifulSoup, представляющий HTML-разметку.
    :return: Список целых чисел - коэффициентов.
    """
    text = soup.get_text()
    match = re.search(
        r"целевой функции F\(X\) =([\s\S]*?)при следующих",
        text,
    )
    if match:
        coefficients_text = match.group(1)
        coefficients = re.findall(r"(\d+)x\d", coefficients_text)
        return [int(coef) for coef in coefficients]
    return []


def find_tables_with_red_highlight(soup: BeautifulSoup) -> List[TableData]:
    """Находит таблицы с красным выделением в HTML-разметке и сохраняет
    информацию о цветовых ячейках, исключая ячейки из последнего столбца
    с заголовком "min".

    :param soup: Объект BeautifulSoup, представляющий HTML-разметку.
    :return: Список объектов TableData, представляющих найденные таблицы.
    """
    tables = soup.find_all("table")
    table_data_list = []

    for table in tables:
        if table.find("td", bgcolor="FFA0A0"):
            rows = table.find_all("tr")
            header = [th.text.strip() for th in rows[0].find_all("td")]
            table_rows = [
                [td.text.strip() for td in row.find_all("td")]
                for row in rows[1:]
            ]
            table_data = TableData(header, table_rows)

            # Находим индекс столбца с заголовком "min"
            min_column_index = header.index("min") if "min" in header else -1

            # Сохраняем информацию о цветовых ячейках, исключая последний столбец "min"
            for row_idx, row in enumerate(rows[1:], start=1):
                for col_idx, cell in enumerate(row.find_all("td")):
                    if (
                        cell.get("bgcolor") == "FFA0A0"
                        and col_idx != min_column_index
                    ):
                        table_data.colored_cells.append(
                            (cell.text.strip(), row_idx, col_idx)
                        )

            table_data_list.append(table_data)

    return table_data_list


def find_last_table(soup: BeautifulSoup) -> TableData:
    """Находит последнюю таблицу в HTML-разметке, следующую за ключевой
    фразой.

    :param soup: Объект BeautifulSoup, представляющий HTML-разметку.
    :return: Объект TableData, представляющий последнюю найденную
        таблицу.
    """
    for br_tag in soup.find_all("br"):
        if br_tag.next_sibling and "Окончательный" in br_tag.next_sibling:
            next_table = br_tag.find_next_sibling("table")
            if next_table:
                rows = next_table.find_all("tr")
                header = [th.text.strip() for th in rows[0].find_all("td")]
                table_rows = [
                    [td.text.strip() for td in row.find_all("td")]
                    for row in rows[1:]
                ]
                table_data = TableData(header, table_rows)
                return table_data

    return TableData([], [])


def parse_html_table_from_soup(
    soup: BeautifulSoup,
) -> Tuple[List[TableData], List[int]]:
    """Парсит HTML-разметку и извлекает таблицы и коэффициенты.

    :param soup: Объект BeautifulSoup, представляющий HTML-разметку.
    :return: Кортеж, содержащий список объектов TableData (для таблиц) и
        список коэффициентов.
    """
    table_data_list = find_tables_with_red_highlight(soup)
    last_table = find_last_table(soup)

    if last_table.header:
        table_data_list.append(last_table)

    coefficients = extract_coefficients_from_soup(soup)

    return table_data_list, coefficients


def process_html_file(html_file: str) -> Tuple[List[TableData], List[int]]:
    """Обрабатывает HTML-файл, извлекает данные таблиц и коэффициенты.

    :param html_file: Путь к HTML-файлу для обработки.
    :return: Кортеж, содержащий список объектов TableData (для таблиц) и
        список коэффициентов.
    """
    with open(html_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    table_data, coefficients = parse_html_table_from_soup(soup)

    return table_data, coefficients


def process_html_folder(
    folder_path: str,
) -> Dict[str, Tuple[List[TableData], List[int]]]:
    """Обрабатывает все HTML-файлы в указанной папке, извлекает данные
    таблиц и коэффициенты для каждого файла.

    :param folder_path: Путь к папке с HTML-файлами для обработки.
    :return: Словарь, где ключ - имя файла, значение - кортеж из списка объектов
        TableData (для таблиц) и списка коэффициентов.
    """
    table_data_all = {}

    for filename in os.listdir(folder_path):
        if filename.endswith(".html"):
            file_path = os.path.join(folder_path, filename)
            table_data_list, coefficients = process_html_file(file_path)
            table_data_all[filename] = (table_data_list, coefficients)

    return table_data_all
