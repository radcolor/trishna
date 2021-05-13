#!/usr/bin/env python3

import os
from __main__ import updater
from telegram.ext import Updater, CommandHandler
from feedparser import parse
from os.path import join

# Func() exec delay
DELAY = int(os.environ["LNG_DELAY"])

# RSS URLs
URLs = [
    'https://sourceforge.net/projects/fakebuilds/rss?path=/havoc',
    'https://sourceforge.net/projects/fakebuilds/rss?path=/RR',
    'https://sourceforge.net/projects/fakecarbon/rss?path=/carbon',
    'https://sourceforge.net/projects/radkernel/rss?path=/'
]

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


# SourceForge releases via RSS feed!
def sourceforge_checker(context):
    for url in URLs:
        req_data = parse(url)
        for i in range(0, len(req_data.entries)):
            title = req_data.entries[i].title.split("/")[2]
            link = req_data.entries[i].link
            date = req_data.entries[i].published
            filesize = int(
                int(req_data.entries[i].media_content[0]["filesize"]) / (1000*1000))

            # Announce the new release.
            if read(title) != title:
                from utils import telegram_helper

                text = '*New SourceForge release found!*\n\n'
                text += 'File size • ' + str(filesize) + 'MB\n'
                text += 'Release date • `' + date + '`\n\n'
                text += 'Download • ' + '[' + title + '](' + link + ')'
                telegram_helper.send_Message(text, "PVT_GRP_CHT")

                # Update the version.
                write(title, title)


# Create a dummy saved file at initial execution
def dummy_file():
    for url in URLs:
        req_data = parse(url)
        for i in range(0, len(req_data.entries)):
            title = req_data.entries[i].title.split("/")[2]
            write(title, title)


dummy_file()
job_queue = updater.job_queue
job_queue.run_repeating(sourceforge_checker, DELAY)
