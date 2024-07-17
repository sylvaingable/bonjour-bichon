import logging

from . import config, nextcloud_client, pictures_chooser, sent_pictures, signal_client

logger = logging.getLogger(__name__)


def send_random_pictures():
    logger.info("Listing available pictures")
    pictures_paths = nextcloud_client.list_pictures()
    logger.info("Listing sent pictures")
    sent_pictures_paths = sent_pictures.ls()
    logger.info("Choosing %s pictures", config.PICTURES_PER_DAY_COUNT)
    chosen_paths = pictures_chooser.choose(
        sent_pictures=sent_pictures_paths, all_pictures=pictures_paths
    )
    logger.info("Retrieving pictures binary content")
    pictures = tuple(nextcloud_client.read_picture(path) for path in chosen_paths)
    logger.info("Sending pictures")
    signal_client.send_message(text=config.PICTURES_MESSAGE, pictures=pictures)
    logger.info("Persisting sent pictures")
    sent_pictures.append(chosen_paths)
    logger.info("Truncating sent pictures journal")
    sent_pictures.truncate(
        keep_last_lines=config.PICTURES_PER_DAY_COUNT * config.HISTORY_DAYS_COUNT
    )


if __name__ == "__main__":
    send_random_pictures()
