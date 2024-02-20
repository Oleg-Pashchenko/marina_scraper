import logging
import dotenv
import os
import dataclasses

from app import file_operations, google_operations

dotenv.load_dotenv()


@dataclasses.dataclass
class GoogleCredentials:
    sheet_id: str
    client_id: str
    secret_key: str


@dataclasses.dataclass
class Config:
    client_tg_name: str
    client_db_url: str
    google_credentials: GoogleCredentials


def get_config():
    return Config(
        client_tg_name=os.getenv('CLIENT_TG_NAME'),
        client_db_url=os.getenv('CLIENT_DATABASE_URL'),
        google_credentials=GoogleCredentials(
            sheet_id=os.getenv('GOOGLE_SHEET_ID'),
            client_id=os.getenv('GOOGLE_CLIENT_ID'),
            secret_key=os.getenv('GOOGLE_SECRET')
        )
    )




logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


def run():
    config = get_config()
    download_status: bool = file_operations.download_file(url=config.client_tg_name,
                                                          filename=config.client_db_url)
    if not download_status:
        return

    convertation_status: bool = file_operations.convert_csv_to_xlsx(config.client_tg_name)
    if not convertation_status:
        return
    google_operations.update_file(config)


run()
"""
schedule.every().day.at("00:00").do(run)
schedule.every().day.at("12:00").do(run)

while True:
    schedule.run_pending()
    time.sleep(10)
"""
