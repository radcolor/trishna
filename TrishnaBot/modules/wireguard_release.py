import requests
from __main__ import updater
from telegram import Bot
from TrishnaBot.modules.sql import rss_records_sql
from TrishnaBot import BOT_TOKEN, MED_DELAY, GIT_FDS_CNL

# Init bot
bot = Bot(BOT_TOKEN)

# WIREGUARD URL
WG_DL_URL = 'https://git.zx2c4.com/wireguard-linux-compat/snapshot/wireguard-linux-compat-'
WG_URL = 'https://build.wireguard.com/distros.txt'
WG_GIT_URL = 'https://git.zx2c4.com/wireguard-linux-compat/log/?h=v'


# WireGuard releases watcher func()
# Based on https://github.com/theradcolor/lazyscripts/blob/master/kernel/wg
def wireguard_releases(context):
    data = requests.get(WG_URL).text.split("\n")

    for x in data:
        if "upstream" in x and "linuxcompat" in x:
            global version
            distro, package, version = x.split()[:3]
            informRelease()


# Announce the new Linux release.
def informRelease():
    if rss_records_sql.get_value("wireguard-current") != version:
        text = '*WireGuard release for Linux 3.10-5.5*\n\n'
        text += 'Git • ' + '[' + "wireguard-linux-compat" + \
            '](' + WG_GIT_URL + version + ')\n'
        text += 'Tag/Version • `v' + version + '`\n\n'
        text += 'Download • ' + '[' + "wireguard-linux-compat" + "-" + \
            version + ".tar.xz" + '](' + WG_DL_URL + version + ".tar.xz" + ')'
        bot.send_message(chat_id=GIT_FDS_CNL, text=text, parse_mode="Markdown", disable_web_page_preview=True)
        rss_records_sql.update_value("wireguard-current", version)


job_queue = updater.job_queue
job_queue.run_repeating(wireguard_releases, MED_DELAY)
