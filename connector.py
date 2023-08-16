import os
import gspread
from datetime import datetime
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
load_dotenv()


class Sheet:
    scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive",
            ]

    def __init__(self, sheet_key: str) -> None:
        self.__credential = ServiceAccountCredentials.from_json_keyfile_dict(create_keyfile_dict(), Sheet.scope)
        self.__worksheet = gspread.authorize(self.__credential).open_by_key(sheet_key).worksheet("Reviews")

    def import_to_sheet(self, message: str) -> None:
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        current_row = len(self.__worksheet.get_all_values())

        new_time_cell = f"A{current_row + 1}"
        new_message_cell = f"B{current_row + 1}"

        self.__worksheet.update(new_time_cell, dt_string)
        self.__worksheet.update(new_message_cell, message)


def create_keyfile_dict():
    variables_keys = {
        "type": os.getenv("SHEET_TYPE"),
        "project_id": os.getenv("SHEET_PROJECT_ID"),
        "private_key_id": os.getenv("SHEET_PRIVATE_KEY_ID"),
        "private_key": os.getenv("SHEET_PRIVATE_KEY"),
        "client_email": os.getenv("SHEET_CLIENT_EMAIL"),
        "client_id": os.getenv("SHEET_CLIENT_ID"),
        "auth_uri": os.getenv("SHEET_AUTH_URI"),
        "token_uri": os.getenv("SHEET_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("SHEET_AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.getenv("SHEET_CLIENT_X509_CERT_URL")
    }
    return variables_keys