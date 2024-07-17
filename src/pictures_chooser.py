from __future__ import annotations

import random

from src import config


def choose(
    sent_pictures: tuple[str, ...],
    all_pictures: tuple[str, ...],
    count: int = config.PICTURES_PER_DAY_COUNT,
) -> tuple[str, ...]:
    """Choose randomly count pictures among all pictures that are not in sent pictures"""
    pictures_count = len(all_pictures)
    chosen_pics = tuple()
    while True:
        random_index = random.randint(0, pictures_count - 1)
        if (
            random_pic := all_pictures[random_index]
        ) not in sent_pictures and random_pic not in chosen_pics:
            chosen_pics += (random_pic,)
        if len(chosen_pics) == count:
            return chosen_pics
