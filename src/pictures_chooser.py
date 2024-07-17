import random

from type_defs import PicturePath


def choose(
    sent_pictures: tuple[PicturePath, ...],
    all_pictures: tuple[PicturePath, ...],
    count: int = 3,
) -> tuple[PicturePath, ...]:
    """Choose randomly count pictures among all pictures that are not in sent pictures"""
    pictures_count = len(all_pictures)
    chosen_pics = tuple()
    while True:
        random_index = random.randint(0, pictures_count - 1)
        if (random_pic := all_pictures[random_index]) not in sent_pictures:
            chosen_pics += (random_pic,)
        if len(chosen_pics) == count:
            return chosen_pics
