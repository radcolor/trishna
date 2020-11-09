#!/usr/bin/env python3

import os
import urllib
from telegram.ext import Updater, CommandHandler
from feedparser import parse
from os.path import join

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
def wireguard_releases():
    # WIREGUARD URL
    WG_URL = 'https://build.wireguard.com/distros.txt'
    file = urllib.request.urlopen(WG_URL)

    for line in file:
        line = line.strip()
        decoded_line = line.decode("utf-8")
        print(decoded_line)
        distro, package, version = line.split()[:3]
        if distro == "upstream" and package == "linuxcompat":
            print(version)


# Main function!
if __name__ == '__main__':
    wireguard_releases()
