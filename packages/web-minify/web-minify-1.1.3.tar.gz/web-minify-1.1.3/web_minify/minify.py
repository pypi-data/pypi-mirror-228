#!/usr/bin/env python3

from .processor import Processor
from .log import setup_logging

from pathos.multiprocessing import cpu_count

import os
import sys

from .modes import Mode, mode2emoji
from .args import parse_arguments
from .logo import logo

from . import __version__

logger = setup_logging(__name__)

scale_factor = 4

nproc = cpu_count() * scale_factor


##############################################################################


def main():
    """
    Commandline entrypoint
    """
    try:
        # fmt:off
        defaults = {
              "mode":"minify"
            , "format": ""
            , "overwrite": False
            , "on_change": False
            , "verbose": False
            , "quiet": False
            , "dry_run": False
            , "force": False
            , "nproc": nproc
            , "size_min": 0
            , "size_max": 100*1024*1024# 100M
            , "gzip": False
            , "sort": False
            , "comments": False
            , "timestamp": False
            , "wrap": False
            , "input": ""
            , "output": ""
            , "copy": False
            , "diff": False
            , "no_size_checks": False
        }
        # fmt:on
        args = vars(parse_arguments(defaults))
        settings = {**defaults, **args}
        verbose = settings.get("verbose", False)
        if verbose:
            logger.info(f"web-minifier version {__version__} started")
        mode = settings.get("mode", "minify")
        settings["mode"] = mode.value if type(mode) is Mode else mode
        processor = Processor(settings)
        logger.info(f"\n{logo}, mode = {mode.value}({mode2emoji(mode.value)})\n")
        res, msg = processor.sanity_checks()
        if not res:
            logger.error(f"Sanity check failed: {msg}, quitting...")
            sys.exit(1)
        if verbose:
            logger.info("Sanity check passed!")
        status, msg = processor.process_files()
        if not status:
            logger.error(f"Processing failed with '{msg}', quitting...")
            sys.exit(1)
        if verbose:
            logger.info("Processing completed successfully!")
        # logger.info(f'\n {"-" * 80} \n Files Processed: {list_of_files}.')
        # logger.info(f'''Number of Files Processed: {len(list_of_files) if isinstance(list_of_files, tuple) else 1}.''')
    except Exception as e:
        logger.error(f"Failed in {os.getcwd()} with {e}")
        raise e
