import logging
import os


def determine_destination_filename(**args) -> tuple:
    local_destination = args.get('share_local')
    filename = args.get('filename')
    filename_array = os.path.split(filename)
    destination_filename = local_destination + filename_array[1] + "_clean"
    args['destination_filename'] = destination_filename
    logging.critical("destination filename: " + destination_filename)
    return False, args


def delete_target_if_exists(**args) -> tuple:
    destination_filename = args.get('destination_filename')
    try:
        os.remove(destination_filename)
    except OSError:
        pass
    return True, args


def set_log_level(**args) -> tuple:
    is_verbose = args.get('is_verbose')
    if is_verbose:
        logging.basicConfig(level="DEBUG", format="%(levelname)s::%(filename)s::%(lineno)s::%(message)s")
    else:
        logging.basicConfig(level="INFO", format="%(levelname)s::%(message)s")
    return True, args




