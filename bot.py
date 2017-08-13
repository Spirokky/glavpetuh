from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from functools import wraps
from core.quotes import Quote
from core.exp import Exp

import logging
import secrets
import config
import datetime


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        username = update.effective_user.username
        if user_id not in config.LIST_OF_ACCESS:
            print("Access denied for {} [{}]".format(username, user_id))
            update.message.reply_text('Пiшов нахуй!', quote=False)
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


def restricted_to_chats(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        chat_id = update.effective_chat.id
        chat_name = update.effective_chat.title
        if chat_id not in config.LIST_OF_GROUPS:
            print("Access denied for {} [{}]".format(chat_name, chat_id))
            update.message.reply_text('Пiшов нахуй!', quote=False)
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


def update_logger(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        now = datetime.datetime.now()
        now = now.strftime('%A, %d. %B %Y %X')
        res = '{}\n[{}]\n{}\n'.format('-'*80, now, update)
        print(res)
        return func(bot, update, *args, **kwargs)
    return wrapped


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


@update_logger
@restricted_to_chats
def help(bot, update):
    update.message.reply_text(config.help_msg, parse_mode="Markdown", quote=False)


@update_logger
def myid(bot, update):
    user = update.effective_user.first_name
    user_id = update.effective_user.id
    update.message.reply_text("{}, {}".format(user, user_id), quote=False)


@update_logger
def ping(bot, update):
    update.message.reply_text('Dev!', quote=False)


@restricted
@restricted_to_chats
@update_logger
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

        update.message.reply_text(res, quote=False)
        return
    else:
        query = quote.get(args[0])

    id, text = query[0], query[1]
    reply = "{}. {}".format(id, text)
    update.message.reply_text(reply, quote=False)


@restricted
@restricted_to_chats
@update_logger
def quote_add(bot, update, args):
    quote = Quote('core/database.db')
    data = " ".join(args)

    if not args:
        return

    try:
        res = quote.add(data)
        id, text = res[0], res[1]
        update.message.reply_text("Цитата № {} добавлена:\n{}".format(id, text), quote=False)
    except Exception as e:
        update.message.reply_text("Не удалось добавить цитату: '%s'" % (e), quote=False)
        return


@restricted
@restricted_to_chats
@update_logger
def quote_remove(bot, update, args):
    quote = Quote('core/database.db')

    if not args:
        return
    else:
        id = args[0]

    try:
        res = quote.remove(id)
        id , text = res[0], res[1]
        update.message.reply_text("Цитата № {} удалена:\n{}".format(id, text), quote=False)
        return
    except Exception as e:
        update.message.reply_text("Не удалось удалить цитату: '%s'" % (e), quote=False)


@update_logger
def next_level(bot, update, args):
    if len(args) == 0:
        update.message.reply_text('Какой левел, ущербный?', quote=False)
        return
    elif len(args) >= 2:
        lvl, percent = args[0], args[1]
    else:
        lvl, percent = args[0], None

    exp = Exp()
    user = update.effective_user.first_name
    res = exp.next_level(lvl, percent)
    output = '{}, {}'
    update.message.reply_text(output.format(user, res), quote=False)


@update_logger
def test(bot, update):
    cmd = update.message.text.strip('/')
    update.message.reply_text('command filter\ncmd: "%s"' % cmd)


def main():
    updater = Updater(secrets.TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('ping', ping))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler('myid', myid))
    dp.add_handler(CommandHandler('quote', quote_get, pass_args=True))
    dp.add_handler(CommandHandler('quoteadd', quote_add, pass_args=True))
    dp.add_handler(CommandHandler('quoteremove', quote_remove, pass_args=True))
    dp.add_handler(CommandHandler('lvl', next_level, pass_args=True))
    dp.add_handler(MessageHandler(Filters.command, test))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    print('Working...')
    main()