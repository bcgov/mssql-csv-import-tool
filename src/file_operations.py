import logging
import time
import os


def determine_destination_filename(**args) -> tuple:
    local_destination = args.get('share_local')
    filename = args.get('filename')
    filename_array = os.path.split(filename)
    destination_filename = local_destination + filename_array[1] + "_clean"
    args['destination_filename'] = destination_filename
    logging.debug("destination filename: " + destination_filename)
    return True, args


def delete_target_if_not_verbose(**args) -> tuple:
    """
    Deletes the destination file if the --verbose flag is set
    and returns True if the file is deleted
    """
    destination_filename = args.get('destination_filename')
    if not args.get('is_verbose'):
        return _delete_file(destination_filename), args
    return True, args


def delete_target(**args) -> tuple:
    """
    Deletes the destination file and returns True
    regardless whether the destination file exists or not
    """
    destination_filename = args.get('destination_filename')
    _delete_file(destination_filename)
    return True, args


def set_log_level(**args) -> tuple:
    is_verbose = args.get('is_verbose')
    if is_verbose:
        logging.basicConfig(level="DEBUG", format="%(levelname)s::%(filename)s::%(lineno)s::%(message)s")
    else:
        logging.basicConfig(level="INFO", format="%(levelname)s::%(message)s")
    return True, args


def wait_for_file_to_finish_writing(**args) -> tuple:
    """
    This wait shouldn't be required but appears to be help with larger files.
    """
    config = args.get('config')
    logging.info("waiting {} seconds for file to finish writing and unlock".format(config.BULK_IMPORT_WAIT))
    time.sleep(config.BULK_IMPORT_WAIT)
    return True, args


def _delete_file(filename: str) -> bool:
    try:
        os.remove(filename)
        return True
    except OSError as e:
        logging.debug(str(e))
        return False




