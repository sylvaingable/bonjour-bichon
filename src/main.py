from . import (
    config,
    image_processor,
    nextcloud_client,
    pictures_chooser,
    sent_pictures,
    signal_client,
)


def send_random_pictures():
    print("Listing available pictures")
    pictures_paths = nextcloud_client.list_pictures()
    print("Listing sent pictures")
    sent_pictures_paths = sent_pictures.ls()
    print(f"Choosing {config.PICTURES_PER_DAY_COUNT} pictures")
    chosen_paths = pictures_chooser.choose(
        sent_pictures=sent_pictures_paths, all_pictures=pictures_paths
    )
    print("Retrieving pictures content")
    pictures = tuple(nextcloud_client.read_picture(path) for path in chosen_paths)
    print("Resizing pictures")
    resized_pictures = tuple(
        image_processor.resize_image(picture) for picture in pictures
    )
    print("Sending pictures")
    signal_client.send_message(text=config.PICTURES_MESSAGE, pictures=resized_pictures)
    print("Persisting sent pictures")
    sent_pictures.append(chosen_paths)
    print("Truncating sent pictures journal")
    sent_pictures.truncate(
        keep_last_lines=config.PICTURES_PER_DAY_COUNT * config.HISTORY_DAYS_COUNT
    )


if __name__ == "__main__":
    send_random_pictures()
