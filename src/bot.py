import datetime
import logging
import yaml
import sys
import pandas as pd

from functools import wraps
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, CallbackQueryHandler)
from telegram.error import (TimedOut, InvalidToken, NetworkError)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from core import (Quote, Exp, Player, render_mpl_table,
                  setup_logging)
from peewee import fn, DoesNotExist

cfg = yaml.safe_load(open('config.yaml', 'rt'))

# Setting up logging stuff
setup_logging()
logger = logging.getLogger('main')

logger.info("Starting...")


def admins(func):
    """
    Restrict access if user is not admin
    """

    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        chat_id = update.effective_chat.id
        title = update.effective_chat.title
        chat_name = "Private chat" if title is None else title
        user_id = update.effective_user.id
        username = update.effective_user.username
        text = update.message.text
        if user_id not in cfg['Telegram']['admins']:
            msg = "Admin access denied for {} ({}) in {} ({}) :: {}"
            msg = msg.format(username, user_id, chat_name, chat_id, text)
            update.message.reply_text('Пiшов нахуй!', quote=False)
            bot.send_message(cfg['Telegram']['mainAdmin'], msg)
            logger.warning(msg)
            return
        return func(bot, update, *args, **kwargs)

    return wrapped


def restricted(func):
    """
    Restrict access if chat is not trusted
    """

    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        print(args)
        chat_id = update.effective_chat.id
        title = update.effective_chat.title
        chat_name = "Private chat" if title is None else title
        user_id = update.effective_user.id
        username = update.effective_user.username
        text = update.message.text
        if chat_id not in cfg['Telegram']['groups']:
            msg = "Group access denied for {} ({}) in {} ({}) :: {}"
            msg = msg.format(username, user_id, chat_name, chat_id, text)
            update.message.reply_text('Пiшов нахуй!', quote=False)
            bot.send_message(cfg['Telegram']['mainAdmin'], msg)
            logger.warning(msg)
            return
        return func(bot, update, *args, **kwargs)

    return wrapped


def update_logger(func):
    """
    Logs updates
    """

    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        chat_id = update.effective_chat.id
        title = update.effective_chat.title
        chat_name = "Private chat" if title is None else title
        user_id = update.effective_user.id
        username = update.effective_user.username
        text = update.message.text
        msg = "{} ({}) :: {} ({}) :: {}"
        msg = msg.format(chat_name, chat_id, username, user_id, text)
        logger.info(msg)
        return func(bot, update, *args, **kwargs)

    return wrapped


def error_handler(bot, update, error):
    try:
        # elogger.error('Update "%s" caused error "%s"' % (update, error))
        pass
    except TimedOut:
        elogger.error('THIS SHIT IS TIMED OUT AGAIN')
    except NetworkError:
        elogger.error('NETWORK SHIT JUST HAPPEND')


@restricted
@update_logger
def show_help(bot, update):
    help_message = """
Доступные команды [бота](https://github.com/Spirokky/glavpetuh):

*/help* - показать это сообщение

*[Эксп]*
*/lvl* `lvl` `%` - показывает сколько опыта осталось до lvl-up
*/exp* `от` `до` - таблица опыта в выбранном диапазоне лвл-ов.

*[Разное]*
*/vote* `текст` - голосование Да/Нет
*/ping* - проверить пульс

*[L2on]*
*/*`nickname` - информация о персонаже с [l2on.net](http://l2on.net)

*[Цитаты]*
*/quote* `id` - показывает случайную цитату или определенную, если указать id
*/quoteadd* `text` - добавить цитату
*/quoteremove* `id` - удалить цитату
"""
    update.message.reply_text(help_message, parse_mode="Markdown",
                              quote=False,
                              disable_notification=True,
                              disable_web_page_preview=True)


@restricted
@update_logger
def myid(bot, update):
    user = update.effective_user.first_name
    user_id = update.effective_user.id
    update.message.reply_text("{}, {}".format(user, user_id),
                              quote=False,
                              disable_notification=True)


@restricted
@update_logger
def ping(bot, update):
    update.message.reply_text('Курлык!',
                              quote=False,
                              disable_notification=True)


@restricted
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


@restricted
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
    data.sort(key=lambda x: x[2], reverse=True)

    if data:
        df = pd.DataFrame()
        df['Имя'] = [x[0] for x in data]
        df['Уровень'] = [x[2] for x in data]
        df['Накачано'] = ["{:>14,}".format(int(x[4])) for x in data]
        df['Проценты'] = ["{} ({})".format(x[5], x[6]) for x in data]
        df['PvP'] = ["{} ({})".format(x[7], x[8]) for x in data]
        df['PK'] = ["{} ({})".format(x[9], x[10]) for x in data]

        try:
            filename = render_mpl_table(df, header_columns=0, col_width=2.0)
            logger.info("Sending photo %s" % filename)
            with open(filename, 'rb') as img:
                bot.send_photo(chat_id=cfg['Telegram']['maingroup'], photo=img)
            return
        except Exception as e:
            logger.error(e)
    else:
        bot.send_message(chat_id=cfg['Telegram']['mainAdmin'],
                         text="Не удалось загрузить данные.")
        return


@restricted
@update_logger
def l2on_get_player(bot, update):
    nickname = update.message.text.strip('/').split()[0]
    player = Player(nickname)
    update.message.reply_text(player.parser(),
                              quote=False,
                              parse_mode="Markdown",
                              disable_web_page_preview=True,
                              disable_notification=True)


@restricted
@update_logger
def vote(bot, update, args):
    msg = ' '.join(args) + '\n'

    keyboard = [[InlineKeyboardButton("Да", callback_data='1'),
                 InlineKeyboardButton("Нет", callback_data='2')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(msg, reply_markup=reply_markup, quote=False)


@restricted
@update_logger
def button(bot, update):
    query = update.callback_query

    if query.data == '1':
        emj = '\u2705 '
    else:
        emj = '\u274C '

    keyboard = [[InlineKeyboardButton("Да", callback_data='1'),
                 InlineKeyboardButton("Нет", callback_data='2')]]

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
                          reply_markup=reply_markup, )


@restricted
@update_logger
def quote_get(bot, update, args):
    output = ''

    if not args:
        query = Quote.select() \
            .order_by(fn.Random()) \
            .limit(1) \
            .get()

        output = query.text

    elif '-a' in args:
        query = Quote.select()
        for q in query:
            output += "[{}] {}\n".format(q.id, q.text)

    else:
        try:
            quote_id = int(args[0])
            query = Quote.get(Quote.id == quote_id)
            output = query.text
        except ValueError:
            query = Quote.select() \
                .order_by(fn.Random()) \
                .limit(1) \
                .get()
            output = query.text
        except DoesNotExist:
            output = "Цитата не найдена"

    update.message.reply_text(output, quote=False)


@admins
@update_logger
def quote_add(bot, update, args):
    if not args:
        output = "Напиши цитату после /quoteadd"
    else:
        new_quote = " ".join(args)
        query = Quote.create(text=new_quote)
        output = "Цитата добавлена:\n{}".format(query.text)

    update.message.reply_text(output, quote=False)


@admins
@update_logger
def quote_remove(bot, update, args):
    if not args:
        update.message.reply_text("Укажи id цитаты после /quoteremove",
                                  quote=False)
        return

    try:
        quote_id = int(args[0])
        quote = Quote.get(Quote.id == quote_id)
        quote_text = quote.text
        quote.delete_instance()
        output = "Цитата удалена:\n[{}] {}".format(quote_id, quote_text)
    except ValueError:
        output = "Укажи id цитаты после /quoteremove"
    except DoesNotExist:
        output = "Цитата не найдена."

    update.message.reply_text(output, quote=False)


def main():
    try:
        updater = Updater(cfg['Telegram']['token'])
        logger.info("Token approved")
    except InvalidToken:
        logger.error('Invalid token')
        sys.exit(0)

    dp = updater.dispatcher

    dp.add_error_handler(error_handler)

    dp.add_handler(CommandHandler('ping', ping))
    dp.add_handler(CommandHandler('help', show_help))
    dp.add_handler(CommandHandler('myid', myid))
    dp.add_handler(CommandHandler('quote', quote_get, pass_args=True))
    dp.add_handler(CommandHandler('quoteadd', quote_add, pass_args=True))
    dp.add_handler(CommandHandler('quoteremove', quote_remove, pass_args=True))
    dp.add_handler(CommandHandler('lvl', next_level, pass_args=True))
    dp.add_handler(CommandHandler('exp', exp_table, pass_args=True))
    dp.add_handler(CommandHandler('vote', vote, pass_args=True))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.command, l2on_get_player))

    queue = updater.job_queue
    queue.run_daily(get_exp_stats_today, datetime.time(hour=7, minute=30))

    updater.start_polling()
    logger.info("Connection established")
    updater.idle()


if __name__ == '__main__':
    main()
