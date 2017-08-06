from telegram.ext import Updater, CommandHandler
import logging
import secrets

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def help(bot, update):
    update.message.reply_text('Help!')


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    updater = Updater(secrets.TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("help", help))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()