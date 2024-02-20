import csv
import logging
from functools import reduce

from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

import pandas as pd
import requests


def process_value(value, column_name):
    replacements = ['<{}>', 'см', 'мм', '(del?) ']
    value = reduce(lambda val, rep: val.replace(rep, ''), replacements, value)

    if column_name == "Цвет":
        return value.strip('{}').split(',')
    else:
        return value


def convert_csv_to_xlsx(filename: str) -> bool:
    logging.info("Начало конвертации CSV в XLSX")

    data = []
    try:
        with open(f'files/{filename}.csv', 'r', encoding='cp1251') as file:
            csv_reader = csv.reader(file, delimiter=';')
            header = next(csv_reader)

            column_indices = {name: header.index(name) for name in header if name in [
                "Наименование", "Код артикула", "Цена", "Краткое описание",
                "Высота", "Глубина", "Ширина", "Тип товаров",
                "Ширина спального места", "Длина спального места", "Цвет", "Изображения товаров"]}

            for row in csv_reader:
                row_data = {column_name: process_value(row[index], column_name) if index < len(row) else None
                            for column_name, index in column_indices.items()}
                if 'Цвет' in row_data and row_data['Цвет']:
                    for color in row_data['Цвет']:
                        d = row_data.copy()
                        d['Цвет'] = color
                        data.append(d)
                else:
                    data.append(row_data)

        df = pd.DataFrame(data)
        df.to_excel(f'files/{filename}.xlsx', index=False, engine='openpyxl')
        logging.info("Конвертация успешно завершена")
        return True
    except FileNotFoundError as e:
        logging.error(f"Файл не найден: {e}")
        return False
    except csv.Error as e:
        logging.error(f"Ошибка чтения CSV файла: {e}")
        return False
    except Exception as e:
        logging.error(f"Произошла ошибка при конвертации: {e}")
        return False


def download_file(url: str, filename: str) -> bool:
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(f'files/{filename}.csv', 'wb') as file:
            file.write(response.content)
        return True

    except (HTTPError, ConnectionError, Timeout, RequestException) as e:
        logging.error(f"Request error: {e}")
        return False

    except OSError as os_err:
        logging.error(f"File system error: {os_err}")
        return False

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return False
