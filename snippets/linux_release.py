#!/usr/bin/env python3

import os
from __main__ import updater
from telegram.ext import Updater, CommandHandler
from feedparser import parse
from os.path import join

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
    KERNEL_GIT_URL = 'https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/log/?h=v'
    KERNEL_DL_URL = 'https://cdn.kernel.org/pub/linux/kernel/v4.x/linux-'
    kernel_list = parse(KERNEL_RSS_URL)

    for i in range (0, len(kernel_list.entries)):
        # Count 4.4(LTS), Mainline and  Stable releases only.
        if '4.4' in kernel_list.entries[i].title or 'stable' in kernel_list.entries[i].title:
            details = kernel_list.entries[i].id.split(',')
            release = details[2].split('.')
            series = release[0] + '.' + release[1]
            append_file = join(series + '-current')
            kernel_version = details[2]

            # Announce the new Linux release.
            if read(append_file) != kernel_version:
                from utils import telegram_helper

                final_name_linux = "linux"
                final_tar_file = "linux-" + kernel_version + ".tar.xz"
                final_git_url = KERNEL_GIT_URL + kernel_version
                final_dl_url = KERNEL_DL_URL + kernel_version + ".tar.xz"

                text = '*Linux new tag for ' + series + ' is released*\n\n'
                text += 'Git • ' + '[' + final_name_linux + '](' + final_git_url + ')\n'
                text += 'Tag/Version • `v' + kernel_version + '`\n'
                text += 'Release date • ' + details[3] + '\n\n'
                text += 'Download • ' + '[' + final_tar_file + '](' + final_dl_url + ')'
                telegram_helper.send_Message(text, "CHNL")

            # Update the version.
            write(append_file, kernel_version)


# Create a dummy saved file at initial execution
def dummy_file():
    # RSS URL from kernel.org
    KERNEL_RSS_URL = 'https://www.kernel.org/feeds/kdist.xml'
    kernel_list = parse(KERNEL_RSS_URL)

    for i in range (0, len(kernel_list.entries)):
        # Count 4.4(LTS), Mainline and  Stable releases only.
        if '4.4' in kernel_list.entries[i].title or 'stable' in kernel_list.entries[i].title:
            details = kernel_list.entries[i].id.split(',')
            release = details[2].split('.')
            series = release[0] + '.' + release[1]
            append_file = join(series + '-current')
            kernel_version = details[2]
            # Append a initial file with version.
            write(append_file, kernel_version)


dummy_file()
job_queue = updater.job_queue
job_queue.run_repeating(linux_releases, DELAY)
