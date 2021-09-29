from __main__ import updater
from telegram import Bot
from feedparser import parse
from TrishnaBot.modules.sql import rss_records_sql
from TrishnaBot import BOT_TOKEN, SHT_DELAY, GIT_FDS_CNL
from os.path import join

# Init bot
bot = Bot(BOT_TOKEN)

# URLs from kernel.org
KERNEL_GIT_URL = 'https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/log/?h=v'
KERNEL_RSS_URL = 'https://www.kernel.org/feeds/kdist.xml'
KERNEL_DL_URL = 'https://cdn.kernel.org/pub/linux/kernel/v%s.x/linux-'


# Linux Kernel releases via RSS feed!
def linux_releases(context):
    kernel_list = parse(KERNEL_RSS_URL)

    for i in range(0, len(kernel_list.entries)):
        # Don't count linux-next
        if not 'linux-next' in kernel_list.entries[i].title:
            global details, release, series, append_file, final_tar_file, final_dl_url
            details = kernel_list.entries[i].id.split(',')
            release = details[2].split('.')
            series = release[0] + '.' + release[1]
            append_file = join(series + '-' + details[1])
            informRelease()


# Announce the new Linux release.
def informRelease():
    if rss_records_sql.get_value(append_file) != details[2]:
        text = '*Linux new tag for ' + series + ' is released*\n\n'
        text += 'Git • ' + '[' + "linux" + '](' + KERNEL_GIT_URL + details[2] + ')\n'
        text += 'Tag/Version • `v' + details[2] + '`\n'
        text += 'Release date • ' + details[3] + '\n\n'
        text += 'Download • ' + '[' + "linux-" + details[2] + ".tar.xz" + \
            '](' + KERNEL_DL_URL % (release[0]) + details[2] + ".tar.xz" + ')'
        bot.send_message(chat_id=GIT_FDS_CNL, text=text, parse_mode="Markdown", disable_web_page_preview=True)
        rss_records_sql.update_value(append_file, details[2])


job_queue = updater.job_queue
job_queue.run_repeating(linux_releases, SHT_DELAY)
