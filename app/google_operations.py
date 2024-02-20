import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials


def update_file(config):
    pass


def upload_xlsx_to_gsheets(gsheet_name, xlsx_path, creds_path):
    # Устанавливаем соединение с Google Sheets
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)

    # Открываем лист Google Sheets
    sheet = client.open(gsheet_name).sheet1

    # Чтение данных из XLSX файла
    df = pd.read_excel(xlsx_path)

    # Очистка существующего содержимого в Google Sheets
    sheet.clear()

    # Запись данных из DataFrame в Google Sheets
    sheet.update([df.columns.values.tolist()] + df.values.tolist())


upload_xlsx_to_gsheets('1EQy13cSuo--q85onQq0UnIfdEKrD5GMN',
                       'marina.xlsx',
                       'google.json')