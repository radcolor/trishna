from telegram import Bot
from __main__ import updater
from TrishnaBot.modules.sql import rss_records_sql
from TrishnaBot import BOT_TOKEN, LNG_DELAY, SNP_GRP_CHT
from feedparser import parse

# Init bot
bot = Bot(BOT_TOKEN)

# RSS URLs
URLs = [
    'https://sourceforge.net/projects/fakebuilds/rss?path=/havoc',
    'https://sourceforge.net/projects/fakebuilds/rss?path=/RR',
    'https://sourceforge.net/projects/fakecarbon/rss?path=/carbon',
    'https://sourceforge.net/projects/radkernel/rss?path=/'
]


# SourceForge releases via RSS feed!
def sourceforge_checker(context):
    for url in URLs:
        req_data = parse(url)
        for i in range(0, len(req_data.entries)):
            global title, link, date, filesize
            title = req_data.entries[i].title.split("/")[2]
            link = req_data.entries[i].link
            date = req_data.entries[i].published
            filesize = int(int(req_data.entries[i].media_content[0]["filesize"]) / (1000*1000))
            informRelease()


def informRelease():
    # Announce the new release.
    if rss_records_sql.get_value(title) != title:
        text = '*New SourceForge release found!*\n\n'
        text += 'File size • ' + str(filesize) + 'MB\n'
        text += 'Release date • `' + date + '`\n\n'
        text += 'Download • ' + '[' + title + '](' + link + ')'
        bot.send_message(chat_id=SNP_GRP_CHT, text=text, parse_mode="Markdown", disable_web_page_preview=True)
        rss_records_sql.update_value(title, title)


job_queue = updater.job_queue
job_queue.run_repeating(sourceforge_checker, LNG_DELAY)
