from telegram.ext import Updater, CommandHandler
from functools import wraps
from core.quotes import Quote

import logging
import secrets
import config


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
    update.message.reply_text(config.help_msg)


def showid(bot, update):
    update.message.reply_text(update.effective_user.id)


def test(bot, update, args):
    s = update.message.text
    update.message.reply_text('got: {} \nargs: {}'.format(s, args))


def quote_get(bot, update, args):
    quote = Quote('core/database.db')

    if not args:
        query = quote.getrandom()

    elif '-a' in args:
        query = quote.get(all=True)
        res = ""

        for item in query:
            id, text = item[0], item[1]
            res += "{}. {}\n".format(id, text)

        update.message.reply_text(res)
        return
    else:
        query = quote.get(args[0])

    id, text = query[0], query[1]
    reply = "{}. {}".format(id, text)
    update.message.reply_text(reply)


@restricted
def quote_add(bot, update, args):
    quote = Quote('core/database.db')
    data = " ".join(args)

    if not args:
        return

    try:
        res = quote.add(data)
        id, text = res[0], res[1]
        update.message.reply_text("Цитата № {} добавлена:\n{}".format(id, text))
    except Exception as e:
        update.message.reply_text("Не удалось добавить цитату: '%s'" % (e))
        return


@restricted
def quote_remove(bot, update, args):
    quote = Quote('core/database.db')

    if not args:
        return
    else:
        id = args[0]

    try:
        res = quote.remove(id)
        id , text = res[0], res[1]
        update.message.reply_text("Цитата № {} удалена:\n{}".format(id, text))
        return
    except Exception as e:
        update.message.reply_text("Не удалось удалить цитату: '%s'" % (e))


def main():
    updater = Updater(secrets.TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler('showid', showid))
    dp.add_handler(CommandHandler('quote', quote_get, pass_args=True))
    dp.add_handler(CommandHandler('quoteadd', quote_add, pass_args=True))
    dp.add_handler(CommandHandler('quoteremove', quote_remove, pass_args=True))
    dp.add_handler(CommandHandler('test', test, pass_args=True))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()