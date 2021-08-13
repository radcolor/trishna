#!/usr/bin/env python3

import os
import subprocess
import logging
import requests
from telegram.ext import Updater, CommandHandler

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

MODE = os.getenv("BOT_MODE")
BOT_TOKEN = os.getenv("BOT_TOKEN")
DRONE_TOKEN = os.getenv("DRONE_TOKEN")

if MODE == "development":
    def run(updater):
        updater.start_polling()
elif MODE == "active":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        APP_NAME = os.environ.get("APP_NAME")
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=BOT_TOKEN,
                              webhook_url="https://{}.herokuapp.com/{}".format(APP_NAME, BOT_TOKEN))
else:
    logger.error("No MODE specified!")
    sys.exit(1)
    

# To execute terminal commands via bot
def shell_handler(update, context):
    user = update.effective_user
    msg = update.effective_message
    if user.id == 1154905452:
        try:
            res = subprocess.Popen(
                context.args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout, stderr = res.communicate()
            result = str(stdout.decode().strip()) + str(stderr.decode().strip())
            if len(result) > 2500:
                with open("output.txt", "w+") as f:
                    f.write(result)
                context.bot.sendDocument(msg.chat.id, open("output.txt", "rb"))
                os.remove("output.txt")
            else:
                update.effective_message.reply_text("<code>" + result + "</code>", parse_mode="html")
        
        except Exception as excp:
            print("Execption!")


# Trigger for other builds using drone.io API
def trigger_handler(update, context):
    user = update.effective_user
    if user.id == 1154905452 or user.id == 869226753 or user.id == 860925514:
        # See if there are 2 arguments passed
        try:
            BRANCH = context.args[1]
        except IndexError:
            update.effective_message.reply_text(
            "Please define a branch/param with format: <code>/trigger repo branch/param</code>", parse_mode="html")
            raise
        REPO = context.args[0]

        # Smoll hack for our kernel repo
        if REPO == "kernel":
            REPO = "android_kernel_xiaomi_whyred"

        # Smoll hack for fakerad
        if REPO == "fakerad":
            REPO = "android_kernel_xiaomi_whyred"
            URL = 'https://cloud.drone.io/api/repos/theradcolor/' + REPO + '/builds?branch=' + BRANCH + '&CI_BRANCH=' + BRANCH + '&CI_KERNEL_TYPE=fakerad' + '&TRIGGERED_CHANNEL=' + '{}'.format(update.effective_chat.id)
        else:
            URL = 'https://cloud.drone.io/api/repos/theradcolor/' + REPO + '/builds?branch=' + BRANCH
        
        drone_header = {"Authorization": "Bearer " + DRONE_TOKEN}
        
        json_out = requests.post(URL, headers=drone_header)

        update.effective_message.reply_text("<code>" + json_out.text + "</code>", parse_mode="html", disable_web_page_preview=True)
    else:
        logger.info("Unauthorised access by {} ".format(update.effective_user["id"]))


# Main function!
if __name__ == '__main__':
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add handler(s)
    dp.add_handler(CommandHandler("exec", shell_handler))
    dp.add_handler(CommandHandler("trigger", trigger_handler))

    # Start CarbonRom release watcher.
    # logger.info("Starting CarbonRom release watcher...")
    # from snippets import carbon_release

    # Start Linux release watcher.
    # logger.info("Starting Linux release watcher...")
    # from snippets import linux_release

    # Start Linux release watcher.
    # logger.info("Starting Site Scraper...")
    # from snippets import site_scrappers

    # Start WireGuard release watcher.
    # logger.info("Starting WireGuard release watcher...")
    # from snippets import wireguard_release
    
    # Start SourceForge release watcher.
    logger.info("Starting SourceForge release watcher...")
    from snippets import sourceforge_checker

    # Start updater
    logger.info("Starting bot...")
    run(updater)
