#!/usr/bin/env python3

import os
from __main__ import updater
from bs4 import BeautifulSoup
import requests

# Func() exec delay
DELAY = int(os.environ["LNG_DELAY"])

# CARBONROM URL
CARBONROM_WHYRED_URL = "https://get.carbonrom.org/device-whyred.html"

# Append file
append_file = "carbonrom-current"

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


# CarbonRom for whyred releases watcher func()
def carbonrom_releases(context):
    req_data = requests.get(CARBONROM_WHYRED_URL).text
    bs4_data = BeautifulSoup(req_data, 'html.parser')
    table_data = bs4_data.find("tbody").find("tr").select("td")

    file_name = table_data[2].find("dd").get_text().strip()
    dl_link = table_data[2].find("dd").find("a")["href"]
    file_size = table_data[3].get_text().strip()
    build_date = table_data[4].get_text().strip()

    # Announce the new Carbon release.
    if read(append_file) != file_name:
        from utils import telegram_helper

        text = '*New Carbon Rom for whyred is released*\n\n'
        text += 'Build Date • `' + build_date + '`\n'
        text += 'Size • `' + file_size + '`\n\n'
        text += 'Download • ' + '[' + file_name + '](' + dl_link + ')'
        telegram_helper.send_Message(text, "PVT_GRP_CHT")

        tag_msg = "@theradcolor"
        telegram_helper.send_Message(tag_msg, "PVT_GRP_CHT")

        # Update the version.
        write(append_file, file_name)


# Create a dummy saved file at initial execution
def dummy_file():
    req_data = requests.get(CARBONROM_WHYRED_URL).text
    bs4_data = BeautifulSoup(req_data, 'html.parser')
    table_data = bs4_data.find("tbody").find("tr").select("td")

    file_name = table_data[2].find("dd").get_text().strip()
    write(append_file, file_name)


dummy_file()
job_queue = updater.job_queue
job_queue.run_repeating(carbonrom_releases, DELAY)
