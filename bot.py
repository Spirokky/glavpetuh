from telegram.ext import Updater
from core import secrets

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

updater = Updater(token=secrets.TOKEN)

dp = updater.dispatcher



def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='wanna talk someshit?')
