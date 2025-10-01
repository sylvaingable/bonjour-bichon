"""
Since there's no official API for Signal, we use an unofficial one that runs a native
client (simulating a user's device) in a Docker container:
https://github.com/bbernhard/signal-cli-rest-api

This module implements a Python wrapper around its REST API:
https://bbernhard.github.io/signal-cli-rest-api/
"""

from __future__ import annotations

import base64
from typing import Iterable
from urllib.parse import urljoin

import httpx

from src import config

_SEND_PATH = "/v2/send"


class SignalError(Exception): ...


def send_message(
    text: str | None = None, pictures: Iterable[bytes] | None = None
) -> None:
    body = {"number": config.SIGNAL_SENDER, "recipients": config.SIGNAL_RECIPIENTS}
    if text is not None:
        body["message"] = text
    if pictures is not None:
        body["base64_attachments"] = [
            base64.b64encode(pic).decode() for pic in pictures
        ]
    try:
        response = httpx.post(
            urljoin(config.SIGNAL_BASE_URL, _SEND_PATH), json=body, timeout=30
        )
        response.raise_for_status()
    except httpx.HTTPError as exc:
        if response := locals().get("response"):
            print(f"Cannot send message: {response.text}")
        raise SignalError("Cannot send message") from exc
