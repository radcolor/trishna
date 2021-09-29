## TrishnaBot

A modular bot written in Python :snake: running on python3 with an sqlalchemy database. Originally madec for personal use for updates, tracking, and for posting stuff. Can be found on telegram also as [Trishna](https://t.me/Trishna_Bot).

### Starting the bot

Install the necessary python dependencies by moving to the project directory and running:

> ```pip3 install -r requirements.txt.```

This will install all necessary python packages.

Once you've setup your database and your configuration (see below) is complete, simply run:

> ```python3 -m TrishnaBot```

### Configuration

```python
MODE = os.getenv("BOT_MODE")
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
DATABASE_URI = os.getenv("DATABASE_URI")
```

### License

TrishnaBot is licensed under the under version 3 of the [GNU GPL License](https://github.com/theradcolor/trishna/blob/master/LICENSE).

The GNU General Public License is a free, copyleft license for software and other kinds of works. When we speak of free software, we are referring to freedom, not price. Our General Public Licenses are designed to make sure that you have the freedom to distribute copies of free software (and charge for them if you wish), that you receive source code or can get it if you want it, that you can change the software or use pieces of it in new free programs, and that you know you can do these things.

Copyright (c) 2021 Shashank. All rights reserved.
