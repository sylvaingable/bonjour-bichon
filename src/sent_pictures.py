from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Generator, Iterable

from src import config


@contextmanager
def ensure_file_exists() -> Generator[None, None, None]:
    path = Path(config.SENT_PICTURES_PATH)
    if not path.exists():
        path.touch()
    yield


@ensure_file_exists()
def ls() -> tuple[str, ...]:
    with open(config.SENT_PICTURES_PATH, "r") as f:
        return tuple(f.read().splitlines())


@ensure_file_exists()
def append(paths: Iterable[str]) -> None:
    with open(config.SENT_PICTURES_PATH, "a+") as f:
        f.writelines(path + "\n" for path in paths)


@ensure_file_exists()
def truncate(keep_last_lines: int = 0) -> None:
    lines_to_keep = ls()[-keep_last_lines:]
    with open(config.SENT_PICTURES_PATH, "w") as f:
        f.truncate()
    if keep_last_lines > 0:
        append(lines_to_keep)
