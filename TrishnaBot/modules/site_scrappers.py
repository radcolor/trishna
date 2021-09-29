import os
import requests
from telegram import Bot
from __main__ import updater
from TrishnaBot.modules.sql import rss_records_sql
from TrishnaBot import BOT_TOKEN, SHT_DELAY, PVT_GRP_CHT
from bs4 import BeautifulSoup

# Init bot
bot = Bot(BOT_TOKEN)

# Other env vars
SSL1 = os.getenv("NOTICE_SCRAPER_LINK")


# Site Scraper func1()
def notice_scraper(context):
    url = requests.get(SSL1)
    soup = BeautifulSoup(url.content, "lxml")

    for a in soup.find_all('a', {"rel": "bookmark"})[:1]:
        global NOTICE_TEXT, FINAL_LINK
        NOTICE_TEXT = a.text
        LINK_TO_NOTICE = a['href'].replace(" ", "%20")

        url = requests.get(LINK_TO_NOTICE)
        soup = BeautifulSoup(url.content, "lxml")
        for a in soup.find_all('a', {"class": "pdfemb-viewer"})[:1]:
            FINAL_LINK = a['href'].replace(" ", "%20")
            informRelease()


# Announce the new notice.
def informRelease():
    if rss_records_sql.get_value(SSL1) != FINAL_LINK:
        text = '*New Notice Found* @theradcolor\n\n'
        text += '[' + NOTICE_TEXT + '](' + FINAL_LINK + ')'
        bot.send_message(chat_id=PVT_GRP_CHT, text=text, parse_mode="Markdown", disable_web_page_preview=True)
        rss_records_sql.update_value(SSL1, FINAL_LINK)


job_queue = updater.job_queue
job_queue.run_repeating(notice_scraper, SHT_DELAY)
