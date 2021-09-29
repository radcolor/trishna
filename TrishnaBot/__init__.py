import os
import logging
import sys
import time

import telegram.ext as tg
from telethon import TelegramClient

StartTime = time.time()

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    logger.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting.",
    )
    quit(1)


# Obtain env vars
MODE = os.getenv("BOT_MODE")

DRONE_TOKEN = os.getenv("DRONE_TOKEN")
DRONE_SERVER = os.getenv("DRONE_SERVER")
DATABASE_URI = os.getenv("DATABASE_URI")

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

SHT_DELAY = int(os.environ["SHT_DELAY"])
MED_DELAY = int(os.environ["MED_DELAY"])
LNG_DELAY = int(os.environ["LNG_DELAY"])

GIT_FDS_CNL = os.getenv("GIT_FDS_CNL")
PVT_GRP_CHT = os.getenv("PVT_GRP_CHT")
SNP_GRP_CHT = os.getenv("SNP_GRP_CHT")
RKW_NGT_CNL = os.getenv("RKW_NGT_CNL")


updater = tg.Updater(BOT_TOKEN, use_context=True)
telethon = TelegramClient("TrishnaBot", API_ID, API_HASH)
dispatcher = updater.dispatcher
