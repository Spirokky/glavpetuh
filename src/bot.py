import datetime
import logging
import sqlite3
import threading

from functools import wraps
from telegram.ext import Updater, CommandHandler, \
    MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from core.exp import Exp
from core.l2on import Player
from core.quotes import Quote
from core import tweelistener
from config import config, secrets

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

db = 'core/database.db'
db_test = 'core/testing_database.db'


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
    update.message.reply_text(config.help_msg, parse_mode="Markdown",
                              quote=False,
                              disable_notification=True,
                              disable_web_page_preview=True)


@update_logger
def myid(bot, update):
    user = update.effective_user.first_name
    user_id = update.effective_user.id
    update.message.reply_text("{}, {}".format(user, user_id),
                              quote=False,
                              disable_notification=True)


@update_logger
def ping(bot, update):
    update.message.reply_text('Курлык!',
                              quote=False,
                              disable_notification=True)


@restricted_to_chats
@update_logger
def quote_get(bot, update, args):
    quote = Quote(db)

    if not args:
        query = quote.getrandom()

    elif '-a' in args:
        query = quote.get(all=True)
        res = ""

        for item in query:
            id, text = item[0], item[1]
            res += "{}. {}\n".format(id, text)

        update.message.reply_text(res,
                                  quote=False,
                                  disable_notification=True)
        return
    else:
        query = quote.get(args[0])

    id, text = query[0], query[1]
    reply = "{}".format(text)
    update.message.reply_text(reply,
                              quote=False,
                              disable_notification=True)


@restricted
@restricted_to_chats
@update_logger
def quote_add(bot, update, args):
    quote = Quote(db)
    data = " ".join(args)

    if not args:
        return

    try:
        res = quote.add(data)
        id, text = res[0], res[1]
        update.message.reply_text("Цитата № {} добавлена:\n{}".format(id, text),
                                  quote=False,
                                  disable_notification=True)
    except Exception as e:
        update.message.reply_text("Не удалось добавить цитату: '%s'" % (e),
                                  quote=False,
                                  disable_notification=True)
        return


@restricted
@restricted_to_chats
@update_logger
def quote_remove(bot, update, args):
    quote = Quote(db)

    if not args:
        return
    else:
        id = args[0]

    try:
        res = quote.remove(id)
        id , text = res[0], res[1]
        update.message.reply_text("Цитата № {} удалена:\n{}".format(id, text),
                                  quote=False,
                                  disable_notification=True)
        return
    except Exception as e:
        update.message.reply_text("Не удалось удалить цитату: '%s'" % (e),
                                  quote=False,
                                  disable_notification=True)


@update_logger
def next_level(bot, update, args):
    if len(args) == 0:
        update.message.reply_text('Какой левел, ущербный?',
                                  quote=False,
                                  disable_notification=True)
        return
    elif len(args) >= 2:
        lvl, percent = int(args[0]), float(args[1])
    else:
        lvl, percent = int(args[0]), None

    exp = Exp()
    user = update.effective_user.first_name
    res = exp.next_level(lvl, percent)
    output = '{}, {}'
    update.message.reply_text(output.format(user, res),
                              quote=False,
                              disable_notification=True)


@update_logger
def exp_table(bot, update, args):
    exp = Exp()

    if len(args) == 0:
        update.message.reply_text(exp.exp_table(),
                                  quote=False,
                                  parse_mode="Markdown",
                                  disable_notification=True)
    elif len(args) >= 2:
        start, end = args[0], args[1]
        update.message.reply_text(exp.exp_table(start, end),
                                  quote=False,
                                  parse_mode="Markdown",
                                  disable_notification=True)
    else:
        start = args[0]
        update.message.reply_text(exp.exp_table(start),
                                  quote=False,
                                  parse_mode="Markdown",
                                  disable_notification=True)


def get_exp_stats_today(bot, update):
    exp = Exp()
    data = exp.get_stats_today()
    res = "```\n"
    res += "{:>3} {:<15} {:<14} {:<16}\n".format('lvl', 'Nickname', 'Накачано', 'Проценты')

    for item in data:
        res += "{:>3} {:<15} {:<14} {:<16}\n".format(item[0], item[1], item[2], item[3])

    res += "```"

    bot.send_message(chat_id=303422193,
                     text=res,
                     parse_mode="Markdown")


@update_logger
def l2on_get_player(bot, update):
    nickname = update.message.text.strip('/').split()[0]
    player = Player(nickname)
    update.message.reply_text(player.parser(),
                              quote=False,
                              parse_mode="Markdown",
                              disable_web_page_preview=True,
                              disable_notification=True)


def get_tweets(bot, job):
    tweet = None
    try:
        connect = sqlite3.connect(db)
        cursor = connect.cursor()

        with connect:
            cursor.execute("SELECT tweet FROM tweets WHERE status = 0;")
            tweet = cursor.fetchall()[-1][0]
            cursor.execute("UPDATE tweets SET status = 1 WHERE status = 0")

    except IndexError:
        pass

    except BaseException as e:
        logger.error(e)

    if tweet:
        bot.send_message(chat_id=-1001105947437,
                         text=tweet,
                         disable_web_page_preview=True)


@update_logger
def vote(bot, update, args):
    msg = ' '.join(args) + '\n'

    keyboard = [[InlineKeyboardButton("Да", callback_data='1'),
                 InlineKeyboardButton("Нет", callback_data='2')],]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(msg, reply_markup=reply_markup, quote=False)


@update_logger
def button(bot, update):
    query = update.callback_query

    if query.data == '1':
        emj = '\u2705 '
    else:
        emj = '\u274C '

    keyboard = [[InlineKeyboardButton("Да", callback_data='1'),
                 InlineKeyboardButton("Нет", callback_data='2')], ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    user = query.from_user.first_name
    msg = query.message.text
    upd = '\n' + emj + user

    v1 = '\n\u2705 ' + user
    v2 = '\n\u274C ' + user

    msg = msg.replace(v1, '')
    msg = msg.replace(v2, '')

    msg += upd

    bot.edit_message_text(text=msg,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup = reply_markup,)


def worker():
    tweelistener.main()


def main():
    logger.info("Starting...")

    updater = Updater(secrets.TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('ping', ping))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler('myid', myid))
    dp.add_handler(CommandHandler('quote', quote_get, pass_args=True))
    dp.add_handler(CommandHandler('quoteadd', quote_add, pass_args=True))
    dp.add_handler(CommandHandler('quoteremove', quote_remove, pass_args=True))
    dp.add_handler(CommandHandler('lvl', next_level, pass_args=True))
    dp.add_handler(CommandHandler('exp', exp_table, pass_args=True))
    dp.add_handler(CommandHandler('vote', vote, pass_args=True))
    dp.add_handler(CommandHandler('stat', get_exp_stats_today))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.command, l2on_get_player))

    dp.add_error_handler(error)

    queue = updater.job_queue
    queue.run_daily(get_exp_stats_today, datetime.time(hour=21, minute=5))
    # queue.run_repeating(get_tweets, interval=5, first=0)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
