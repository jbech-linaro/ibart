# -*- coding: utf-8 -*-
import logging as log
import signal
import sys
import time

###############################################################################
# Sigint
###############################################################################


def signal_handler(signal, frame):
    log.debug("Gracefully killed!")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

###############################################################################
# Time
###############################################################################


def get_running_time(time_start):
    """Returns the running time on format: <hours>h:<minutes>m:<seconds>s."""
    m, s = divmod(time.time() - time_start, 60)
    h, m = divmod(m, 60)
    return "{}h:{:02d}m:{:02d}s".format(int(h), int(m), int(s))
