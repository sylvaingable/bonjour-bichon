from __future__ import annotations

from typing import Iterable

from type_defs import PicturePath

from src import config


def ls() -> tuple[PicturePath, ...]:
    with open(config.SENT_PICTURES_PATH, "r") as f:
        return tuple(f.read().splitlines())


def append(paths: Iterable[PicturePath]) -> None:
    with open(config.SENT_PICTURES_PATH, "a+") as f:
        f.writelines(path + "\n" for path in paths)


def truncate(keep_last_lines: int = 0) -> None:
    lines_to_keep = ls()[-keep_last_lines:]
    with open(config.SENT_PICTURES_PATH, "w") as f:
        f.truncate()
    if keep_last_lines > 0:
        append(lines_to_keep)
