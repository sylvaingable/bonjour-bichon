import os

from dotenv import load_dotenv

load_dotenv()

HISTORY_DAYS_COUNT = int(os.getenv("HISTORY_DAYS_COUNT"))  # type: ignore
PICTURES_PER_DAY_COUNT = int(os.getenv("PICTURES_PER_DAY_COUNT"))  # type: ignore
PICTURES_MESSAGE = str(os.getenv("PICTURES_MESSAGE"))
NEXTCLOUD_WEBDAV_URL = str(os.getenv("NEXTCLOUD_WEBDAV_URL"))
NEXTCLOUD_USERNAME = str(os.getenv("NEXTCLOUD_USERNAME"))
NEXTCLOUD_PASSWORD = str(os.getenv("NEXTCLOUD_PASSWORD"))
NEXTCLOUD_PHOTOS_PATH = str(os.getenv("NEXTCLOUD_PHOTOS_PATH"))
SENT_PICTURES_PATH = str(os.getenv("SENT_PICTURES_PATH"))
SIGNAL_BASE_URL = str(os.getenv("SIGNAL_BASE_URL"))
SIGNAL_SENDER = str(os.getenv("SIGNAL_SENDER"))
SIGNAL_RECIPIENTS = str(os.getenv("SIGNAL_RECIPIENTS")).split(",")
