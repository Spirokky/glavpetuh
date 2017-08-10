from telegram.ext import Updater, CommandHandler
from functools import wraps

import logging
import secrets


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

LIST_OF_ACCESS = [303422193]


def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ACCESS:
            print("Unauthorized access denied for {}.".format(user_id))
            update.message.reply_text('Недостаточно прав.')
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def help(bot, update):
    pass


def showid(bot, update):
    update.message.reply_text(update.effective_user.id)


def quote(bot, update):
    pass


def quoteadd(bot, update):
    pass


def quoteremove(bot, update):
    pass


def main():
    updater = Updater(secrets.TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler('showid', showid))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()