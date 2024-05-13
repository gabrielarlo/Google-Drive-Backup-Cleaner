import os
import schedule
import time
import logging
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

SERVICE_ACCOUNT_FILE = "service_account.json"
scopes = ["https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
drive_service = build("drive", "v3", credentials=creds)
folder_ids = [
    "1HivNYRlfz1tin9xHXt6_7SKSpSxSGs2W",
    "1ryssuYZcg-KZ9xLhfP5OYkkKGlIjJ8n2",
    "14mBL7woZY0V52qwd2LVxIb-2doY4Mms1",
]


def cleanup_old_files():
    print("Cleaning up old files...")
    cutoff_date = datetime.now() - timedelta(days=30)

    for folder_id in folder_ids:
        query = f"'{folder_id}' in parents and trashed = false"
        try:
            results = (
                drive_service.files()
                .list(q=query, fields="nextPageToken, files(id, name, modifiedTime)")
                .execute()
            )
            items = results.get("files", [])
            for item in items:
                modified_time = datetime.strptime(
                    item["modifiedTime"], "%Y-%m-%dT%H:%M:%S.%fZ"
                )
                if modified_time < cutoff_date:
                    logging.info(
                        f"Deleting file: {item['name']} (Modified: {modified_time}) from folder: {folder_id}"
                    )
                    drive_service.files().delete(fileId=item["id"]).execute()
        except Exception as e:
            logging.error(f"An error occurred: {e}")


schedule.every().day.at("03:00").do(cleanup_old_files)

while True:
    schedule.run_pending()
    time.sleep(60)
