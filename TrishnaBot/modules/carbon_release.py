import requests
from telegram import Bot
from __main__ import updater
from TrishnaBot.modules.sql import rss_records_sql
from TrishnaBot import BOT_TOKEN, LNG_DELAY, SNP_GRP_CHT
from bs4 import BeautifulSoup

# Init bot
bot = Bot(BOT_TOKEN)

# CARBONROM URL
CARBONROM_WHYRED_URL = "https://get.carbonrom.org/device-whyred.html"


# CarbonRom for whyred releases watcher func()
def carbonrom_releases(context):
    req_data = requests.get(CARBONROM_WHYRED_URL).text
    bs4_data = BeautifulSoup(req_data, 'html.parser')
    table_data = bs4_data.find("tbody").find("tr").select("td")
    global file_name, dl_link, file_size, build_date
    file_name = table_data[2].find("dd").get_text().strip()
    dl_link = table_data[2].find("dd").find("a")["href"]
    file_size = table_data[3].get_text().strip()
    build_date = table_data[4].get_text().strip()
    informRelease()


def informRelease():
    # Announce the new Carbon release.
    if rss_records_sql.get_value("carbonrom-current") != file_name:
        text = '*New Carbon Rom for whyred is released*\n\n'
        text += 'Build Date • `' + build_date + '`\n'
        text += 'Size • `' + file_size + '`\n\n'
        text += 'Download • ' + '[' + file_name + '](' + dl_link + ')'
        bot.send_message(chat_id=SNP_GRP_CHT, text=text, parse_mode="Markdown")

        tag_msg = "@fakeyatogod @imudayveer @Nuub073 @theradcolor"
        bot.send_message(chat_id=SNP_GRP_CHT, text=tag_msg, parse_mode="Markdown", disable_web_page_preview=True)
        rss_records_sql.update_value("carbonrom-current", file_name)


job_queue = updater.job_queue
job_queue.run_repeating(carbonrom_releases, LNG_DELAY)
