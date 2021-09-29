import os
from telegram.ext import Updater, CommandHandler

from TrishnaBot import (
    telethon,
    dispatcher,
    updater,
    MODE,
    BOT_TOKEN,
    logger
)


def start(update, context):
    update.effective_message.reply_text("Hey there, I'm Trishna", parse_mode="html")


def main():
    start_handler = CommandHandler("start", start, pass_args=True)

    dispatcher.add_handler(start_handler)
    if MODE == "development":
        updater.start_polling()
    elif MODE == "active":
        PORT = int(os.environ.get("PORT", "8443"))
        APP_NAME = os.environ.get("APP_NAME", "TrishnaBot")
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=BOT_TOKEN,
                              webhook_url="https://{}.herokuapp.com/{}".format(APP_NAME, BOT_TOKEN))

    telethon.run_until_disconnected()
    updater.idle()


if __name__ == "__main__":
    telethon.start(bot_token=BOT_TOKEN)
    
    # Start DB
    logger.info("Starting DB...")
    from TrishnaBot.modules.sql import rss_records_sql

    # Start CarbonRom release watcher.
    logger.info("Starting CarbonRom release watcher...")
    from TrishnaBot.modules import carbon_release

    # Start Linux release watcher.
    logger.info("Starting Linux release watcher...")
    from TrishnaBot.modules import linux_release

    # Start Linux release watcher.
    logger.info("Starting Site Scraper...")
    from TrishnaBot.modules import site_scrappers

    # Start WireGuard release watcher.
    logger.info("Starting WireGuard release watcher...")
    from TrishnaBot.modules import wireguard_release

    # Start Trigger Handler Scrapper.
    logger.info("Starting Trigger Handler...")
    from TrishnaBot.modules import dronetrigger_handler
    
    # Start SourceForge release watcher.
    # logger.info("Starting SourceForge release watcher...")
    # from TrishnaBot.modules import sourceforge_checker

    main()
