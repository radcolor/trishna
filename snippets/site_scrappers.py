#!/usr/bin/env python3

import os
import requests
from __main__ import updater
from telegram.ext import Updater, CommandHandler
from bs4 import BeautifulSoup

# Func() exec delay
DELAY = int(os.environ["SHT_DELAY"])

# Other env vars
SSL1 = os.getenv("NOTICE_SCRAPER_LINK")

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


# Site Scraper func1()
def notice_scraper(context):
    url = requests.get(SSL1)
    soup = BeautifulSoup(url.content, "lxml")
    
    for a in soup.find_all('a', {"rel": "bookmark"})[:1]:
        LINK_TO_NOTICE = a['href'].replace(" ", "%20")
        
        url = requests.get(LINK_TO_NOTICE)
        soup = BeautifulSoup(url.content,"lxml")
        for a in soup.find_all('a', {"class": "pdfemb-viewer"})[:1]:
            FINAL_LINK = a['href'].replace(" ", "%20")
            if read("site_scraper_notice") != FINAL_LINK:
                from utils import telegram_helper
                
                text = '*New Notice Found* @theradcolor\n\n'
                text += FINAL_LINK
                telegram_helper.send_Message(text, "PVT_GRP_CHT")
                
                # Update the version.
                write("site_scraper_notice", FINAL_LINK)


# Create a dummy saved file at initial execution
def dummy_file():
    url = requests.get(SSL1)
    soup = BeautifulSoup(url.content, "lxml")
    for a in soup.find_all('a', {"rel": "bookmark"})[:1]:
        LINK_TO_NOTICE = a['href'].replace(" ", "%20")
        url = requests.get(LINK_TO_NOTICE)
        soup = BeautifulSoup(url.content,"lxml")
        for a in soup.find_all('a', {"class": "pdfemb-viewer"})[:1]:
            FINAL_LINK = a['href'].replace(" ", "%20")
            write("site_scraper_notice", FINAL_LINK)


# dummy_file()
job_queue = updater.job_queue
job_queue.run_repeating(notice_scraper, DELAY)