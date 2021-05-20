#!/usr/bin/env python3

import os
import requests
from __main__ import updater
from telegram.ext import Updater, CommandHandler
from feedparser import parse
from os.path import join

# Func() exec delay
DELAY = int(os.environ["MED_DELAY"])

# WIREGUARD URL
WG_URL = 'https://build.wireguard.com/distros.txt'
WG_GIT_URL = 'https://git.zx2c4.com/wireguard-linux-compat/log/?h=v'
WG_DL_URL = 'https://git.zx2c4.com/wireguard-linux-compat/snapshot/wireguard-linux-compat-'

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
    data = requests.get(WG_URL).text.split("\n")
    
    for x in data:
        if "upstream" in x and "linuxcompat" in x:
            distro, package, version = x.split()[:3]
            append_file = "wireguard-current"

            # Announce the new WireGuard release.
            if read(append_file) != version:
                from utils import telegram_helper

                final_name = "wireguard-linux-compat"
                final_tar_file = final_name + "-" + version + ".tar.xz"
                final_git_url = WG_GIT_URL + version
                final_dl_url = WG_DL_URL + version + ".tar.xz"

                text = '*WireGuard release for Linux 3.10-5.5*\n\n'
                text += 'Git • ' + '[' + final_name + '](' + final_git_url + ')\n'
                text += 'Tag/Version • `v' + version + '`\n\n'
                text += 'Download • ' + '[' + final_tar_file + '](' + final_dl_url + ')'
                telegram_helper.send_Message(text, "GIT_FDS_CNL")
                telegram_helper.send_Message(text, "PVT_GRP_CHT")

            # Update the version.
            write(append_file, version)


# Create a dummy saved file at initial execution
def dummy_file():
    data = requests.get(WG_URL).text.split("\n")
    
    for x in data:
        if "upstream" in x and "linuxcompat" in x:
            distro, package, version = x.split()[:3]
            append_file = "wireguard-current"
            # Append a initial file with version.
            write(append_file, version)


dummy_file()
job_queue = updater.job_queue
job_queue.run_repeating(wireguard_releases, DELAY)
