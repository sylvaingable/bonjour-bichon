import os

from dotenv import load_dotenv

load_dotenv()

NEXTCLOUD_WEBDAV_URL = str(os.getenv("NEXTCLOUD_WEBDAV_URL"))
NEXTCLOUD_USERNAME = str(os.getenv("NEXTCLOUD_USERNAME"))
NEXTCLOUD_PASSWORD = str(os.getenv("NEXTCLOUD_PASSWORD"))
NEXTCLOUD_PHOTOS_PATH = str(os.getenv("NEXTCLOUD_PHOTOS_PATH"))
SENT_PICTURES_PATH = str(os.getenv("SENT_PICTURES_PATH"))
SIGNAL_BASE_URL = str(os.getenv("SIGNAL_BASE_URL"))
SIGNAL_SENDER = str(os.getenv("SIGNAL_SENDER"))
SIGNAL_RECIPIENTS = str(os.getenv("SIGNAL_RECIPIENTS")).split(",")
