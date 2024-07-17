from __future__ import annotations

import atexit
from io import BytesIO

from webdav4 import client as webdav_client

from src import config

_client = webdav_client.Client(
    config.NEXTCLOUD_WEBDAV_URL,
    auth=(config.NEXTCLOUD_USERNAME, config.NEXTCLOUD_PASSWORD),
)
# webdav4.client.Client uses an httpx client that should be closed on exit
atexit.register(lambda webdav_client: webdav_client.http.close(), _client)


class PictureError(Exception): ...


def list_pictures() -> tuple[str, ...]:
    try:
        return tuple(
            el["href"]  # type: ignore
            for el in _client.ls(config.NEXTCLOUD_PHOTOS_PATH)
            if el["type"] == "file"  # type: ignore
        )
    except webdav_client.ClientError as exc:
        raise PictureError("Cannot list files") from exc


def read_picture(path: str) -> bytes:
    file_obj = BytesIO()
    try:
        _client.download_fileobj(from_path=path, file_obj=file_obj)
        return file_obj.getvalue()
    except webdav_client.ClientError as exc:
        raise PictureError("Cannot read file") from exc
