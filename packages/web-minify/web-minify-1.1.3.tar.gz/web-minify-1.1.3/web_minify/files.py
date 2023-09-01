import os
from time import sleep
from .handlers import HandlerManager
import pprint
import logging

logger = logging.getLogger(__name__)


file_endings = None


def generate_file_list(folder: str, target: tuple = (), omit: tuple = (), allow_hidden: bool = False, topdown: bool = True, onerror: object = None, followlinks: bool = False) -> tuple:
    oswalk = os.walk(folder, topdown=topdown, onerror=onerror, followlinks=followlinks)
    return [
        os.path.abspath(os.path.join(root, file))
        for root, dirs, files in oswalk
        for file in files
        if not file.startswith(() if allow_hidden else ".") and not file.endswith(omit)
        #        and (f.endswith(target) if target else True)
    ]


def path_is_in_path(path_a, path_b):
    if not path_a or not path_b:
        return False
    return os.path.abspath(path_a) == os.path.commonpath([os.path.abspath(path_a), os.path.abspath(path_b)])


def watch_files(file_path, settings: dict):
    logger.info(f"Watch is not suppoerted yet!")


def old_watch_files(file_path, settings: dict):
    """Process multiple CSS, JS, HTML files with multiprocessing."""
    logger.info(f"Process {os.getpid()} is Compressing {file_path}.")
    processor = Processor(settings)
    res, msg = processor.sanity_checks()
    if not res:
        logger.error("Sanity check failed: {msg}, quitting...")
        sys.exit(1)
    if settings.get("watch", False):
        previous = int(os.stat(file_path).st_mtime)
        logger.info(f"Process {os.getpid()} is Watching {file_path}.")
        # logger.info(f'Total Maximum CPUs used: ~{cpu_count()} Cores.')
        #        pool = Pool(cpu_count())  # Multiprocessing Async
        #        pool.map_async(partial(
        #                watch_files, settings=args),
        #           list_of_files)
        #      pool.close()
        #     pool.join()
        while True:
            actual = int(os.stat(file_path).st_mtime)
            if previous == actual:
                sleep(60)
            else:
                previous = actual
                logger.info(f"Modification detected on {file_path}.")
                processor.process_file(file_path, file_path)
    else:
        processor.process_file(file_path, file_path)


def determine_file_extension(file_path: str):
    global file_endings
    if not file_path:
        return None, False
    index = file_path.rfind(".")
    if index < 0:
        return None, False
    file_ending = file_path[index + 1 :]
    if not file_ending:
        return None, False
    if not file_endings:
        handlers = HandlerManager()
        file_endings = handlers.get_supported_extensions()
    return file_ending, file_ending in file_endings


def read_file(fname, strip=True):
    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    data = ""
    if os.path.exists(fn):
        with open(fn) as f:
            data = f.read()
            data = data.strip() if strip else data
            # logger.info(f"Got data '{data}' from '{fn}'")
    else:
        logger.error(f"Could not find file {fn}")
        logger.warning(f"NOTE: Current working directory is {os.getcwd()}")
    return data
