import logging
import os
from src.config import Config


logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)


def determine_destination_filename(**args) -> tuple:
    destination_path = args.get('windows_share_from_db_perspective')
    args['destination_filename'] = args.get('filename') + "_clean"
    return True, args


def delete_target_if_exists(**args) -> tuple:
    destination_filename = args.get('destination_filename')
    try:
        os.remove(destination_filename)
    except OSError:
        pass
    return True, args





