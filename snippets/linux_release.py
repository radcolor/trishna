#!/usr/bin/env python3

import os
from __main__ import updater
from telegram.ext import Updater, CommandHandler
from feedparser import parse
from os.path import join

CNL_ID = os.getenv("CHANNEL_ID")
CHT_ID = os.getenv("CHAT_ID")
PVT_GRP_ID = os.getenv("PVT_CHAT_ID")
DELAY = int(os.environ["WATCH_DELAY"])

# Read appended text func() from a file
def read(file):
    try:
        file = open(file, 'r')
        data = file.read()
        file.close()

    except FileNotFoundError:
        data = None

    return data


# Append text func() to a file
def write(file, data):
    file = open(file, 'w+')
    file.write(data)
    file.close()


# Linux Kernel releases via RSS feed!
def linux_releases(context):
    # RSS URL from kernel.org
    KERNEL_RSS_URL = 'https://www.kernel.org/feeds/kdist.xml'
    kernel_list = parse(KERNEL_RSS_URL)

    for i in range (0, len(kernel_list.entries)):
        # Count 4.4(LTS), Mainline and  Stable releases only.
        if '4.4' in kernel_list.entries[i].title or 'mainline' in kernel_list.entries[i].title or 'stable' in kernel_list.entries[i].title:
            details = kernel_list.entries[i].id.split(',')
            release = details[2].split('.')
            series = release[0] + '.' + release[1]
            append_file = join(series + '-current')
            kernel_version = details[2]

            # Announce the new Linux release.
            if read(append_file) != kernel_version:
                from utils import telegram_helper
                telegram_helper.send_Message("*New Tag for Linux *" + series + "* is released!* \n\n"
                + "*Version: *" + kernel_version, "PVT_GRP")

            # Update the version.
            write(append_file, kernel_version)


job_queue = updater.job_queue
job_queue.run_repeating(linux_releases, DELAY)
