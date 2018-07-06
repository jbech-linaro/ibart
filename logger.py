# -*- coding: utf-8 -*-
import glob
import logging as log
import os
import re
import zipfile

from collections import OrderedDict
from pathlib import Path

# Local modules
import github
import settings

PRE_CLONE = 0
CLONE = 1
POST_CLONE = 2
PRE_BUILD = 3
BUILD = 4
POST_BUILD = 5
PRE_FLASH = 6
FLASH = 7
POST_FLASH = 8
PRE_BOOT = 9
BOOT = 10
POST_BOOT = 11
PRE_TEST = 12
TEST = 13
POST_TEST = 14

log2str = {
        PRE_CLONE: "pre_clone",
        CLONE: "clone",
        POST_CLONE: "post_clone",

        PRE_BUILD: "pre_build",
        BUILD: "build",
        POST_BUILD: "post_build",

        PRE_FLASH: "pre_flash",
        FLASH: "flash",
        POST_FLASH: "post_flash",

        PRE_BOOT: "pre_boot",
        BOOT: "boot",
        POST_BOOT: "post_boot",

        PRE_TEST: "pre_test",
        TEST: "test",
        POST_TEST: "post_test"
        }

# -----------------------------------------------------------------------------
# Log handling
# -----------------------------------------------------------------------------


def get_logs(pr_full_name, pr_number, pr_id, pr_sha1):
    """The function returns a dictionary with dictionaries where the high level
       dictionary have 'key' corresponding job definition and the inner
       dictionaries corresponds to each individual log files."""
    if (pr_full_name is None or pr_number is None or pr_id is None or
            pr_sha1 is None):
        log.error("Cannot store log file (missing parameters)")
        return

    log_file_dir = "{p}/{fn}/{n}/{i}/{s}".format(
            p=settings.log_dir(), fn=pr_full_name, n=pr_number, i=pr_id,
            s=pr_sha1)

    log.debug("Getting logs from folder: {}".format(log_file_dir))

    all_logs = OrderedDict()
    for zf in sorted(glob.glob("{}/*.zip".format(log_file_dir))):
        logs = OrderedDict()
        log.debug("Unpacking zip-file: {}".format(zf))
        for key, logtype in log2str.items():
            filename = "{}.log".format(logtype)
            logs[logtype] = read_log(filename, zf)
        # Use job definition as key when returning logs from multi definition
        # jobs.
        jd = Path(zf).name.replace(".zip", "")
        all_logs[jd] = logs
    return all_logs


def read_log(filename, zip_file):
    """This function extracts a single log file from a certain zip-file."""
    if filename is None or zip_file is None:
        log.error("Cannot read log file (missing parameters)")
        return

    log_line = ""
    try:
        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        # TODO: Get rid of "logs/"
        filename = "logs/{}".format(filename)
        with zipfile.ZipFile(zip_file) as myzip:
            with myzip.open(filename) as myfile:
                log_line = ansi_escape.sub('', myfile.read().decode('utf-8'))
    except (IOError, KeyError) as e:
        pass

    # Add line numbers to the log
    ctr = 1
    numbered_log = []
    for l in log_line.split('\n'):
        numbered_log.append("{:>6}:  {}".format(ctr, l))
        ctr += 1

    # If there is no content in the log, then don't return anything
    if len(numbered_log) == 1 and len(numbered_log[0]) == 9:
        return None

    return "\n".join(numbered_log)


def clear_logfiles(payload):
    if payload is None:
        log.error("Cannot clear log file (missing parameters)")
        return

    pr_full_name = github.pr_full_name(payload)
    pr_number = github.pr_number(payload)
    pr_id = github.pr_id(payload)
    pr_sha1 = github.pr_sha1(payload)

    log_file_dir = "{p}/{fn}/{n}/{i}/{s}".format(
            p=settings.log_dir(), fn=pr_full_name, n=pr_number, i=pr_id,
            s=pr_sha1)

    for zf in glob.glob("{}/*.zip".format(log_file_dir)):
        if os.path.isfile(zf):
            os.remove(zf)


def store_logfile(payload, current_file, full_log_file):
    if (payload is None or current_file is None or full_log_file is None):
        log.error("Cannot store log file (missing parameters)")
        return

    pr_full_name = github.pr_full_name(payload)
    pr_number = github.pr_number(payload)
    pr_id = github.pr_id(payload)
    pr_sha1 = github.pr_sha1(payload)

    log_file_dir = "{p}/{fn}/{n}/{i}/{s}".format(
            p=settings.log_dir(), fn=pr_full_name, n=pr_number, i=pr_id,
            s=pr_sha1)

    try:
        os.stat(log_file_dir)
    except FileNotFoundError:
        os.makedirs(log_file_dir)

    source = current_file
    dest = "{d}/{f}".format(d=log_file_dir, f=full_log_file)

    try:
        zipfile.ZipFile(dest, mode='a',
                        compression=zipfile.ZIP_DEFLATED).write(source)
    except FileNotFoundError:
        log.error("Couldn't find file {}".format(dest))
