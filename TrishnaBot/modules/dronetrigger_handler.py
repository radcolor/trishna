import requests
from telegram.ext import CommandHandler
from telegram import Bot
from TrishnaBot import dispatcher, BOT_TOKEN, DRONE_SERVER, DRONE_TOKEN, logger

# Init bot
bot = Bot(BOT_TOKEN)


# Trigger for other builds using drone.io API
def trigger_drone(update, context):
    user = update.effective_user
    if user.id == 1154905452 or user.id == 869226753 or user.id == 860925514:
        # See if there are 2 arguments passed
        try:
            REPO = context.args[0]
            BRANCH = context.args[1]
        except IndexError:
            update.effective_message.reply_text(
                "Please trigger with format: <code>/trigger repo_name branch_name other_params(optional)</code>", parse_mode="html")
            raise

        # Smoll hack for our kernel repo
        if REPO == "kernel":
            REPO = "android_kernel_xiaomi_whyred"

        # Smoll hack for fakerad
        if REPO == "fakerad":
            REPO = "android_kernel_xiaomi_whyred"
            URL = DRONE_SERVER + 'api/repos/theradcolor/' + REPO + '/builds?branch=' + BRANCH + '&CI_BRANCH=' + BRANCH + '&CI_KERNEL_TYPE=fakerad' + '&TRIGGERED_CHANNEL=' + '{}'.format(update.effective_chat.id)
        else:
            URL = DRONE_SERVER + 'api/repos/theradcolor/' + REPO + '/builds?branch=' + BRANCH

        drone_header = {"Authorization": "Bearer " + DRONE_TOKEN}
        json_out = requests.post(URL, headers=drone_header)

        update.effective_message.reply_text("<code>" + json_out.text + "</code>", parse_mode="html", disable_web_page_preview=True)
    else:
        logger.info("Unauthorised access by {} ".format(
            update.effective_user["id"]))


trigger_handler = CommandHandler("trigger", trigger_drone, pass_args=True)
dispatcher.add_handler(trigger_handler)
