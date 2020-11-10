#!/usr/bin/env python3

import os
import requests
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


# WireGuard releases watcher func()
# Based on https://github.com/theradcolor/lazyscripts/blob/master/kernel/wg
def wireguard_releases(context):
    # WIREGUARD URL
    WG_URL = 'https://build.wireguard.com/distros.txt'

    data = requests.get(WG_URL).text.split("\n")
    
    for x in data:
        if "upstream" in x and "linuxcompat" in x:
            distro, package, version = x.split()[:3]
            append_file = "wireguard-current"

            # Announce the new WireGuard release.
            if read(append_file) != version:
                from utils import telegram_helper
                telegram_helper.send_Message("*New WireGuard for Linux 3.10-5.5 is released!*\n\n"
                + "*Version: *v" + version, "PVT_GRP")

            # Update the version.
            write(append_file, version)


job_queue = updater.job_queue
job_queue.run_repeating(wireguard_releases, DELAY)
