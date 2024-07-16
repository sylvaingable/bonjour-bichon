from __future__ import annotations

import atexit
from typing import NamedTuple

from webdav4 import client as webdav_client

from src import config

_client = webdav_client.Client(
    config.NEXTCLOUD_WEBDAV_URL,
    auth=(config.NEXTCLOUD_USERNAME, config.NEXTCLOUD_PASSWORD),
)
# webdav4.client.Client uses an httpx client that should be closed on exit
atexit.register(lambda webdav_client: webdav_client.http.close(), _client)


class PictureException(Exception): ...


class PicturePath(NamedTuple):
    path: str


def list_pictures() -> tuple[PicturePath]:
    try:
        return tuple(
            PicturePath(el["href"])
            for el in _client.ls(config.NEXTCLOUD_PHOTOS_PATH)
            if el["type"] == "file"
        )
    except webdav_client.ClientError as exc:
        raise PictureException("Cannot list pictures") from exc
