import ublydok
import telepot
import sys
import time
import l2onparser
import urllib3
import json
import config

from pprint import pprint
from urllib.parse import unquote
from urllib import request


# ------ Magic for PythonAnywhere free account ------ 
# proxy_url = "http://proxy.server:3128"
# telepot.api._pools = {
#     'default': urllib3.ProxyManager(proxy_url=proxy_url,
#                                   num_pools=3, maxsize=10,
#                                   retries=False, timeout=30),
# }
# telepot.api._onetime_pool_spec = (urllib3.ProxyManager,
#                                   dict(proxy_url=proxy_url, num_pools=1,
#                                   maxsize=1, retries=False, timeout=30))
# ------ end of magic ------

TOKEN = sys.argv[1]
TRUSTED = [-188672102,  # testdebug
           303422193,   # Spirokky's private
           -1001105947437,]  # back to l2 ]

bot = telepot.Bot(TOKEN)

daddy = 'http://i.imgur.com/b8XZVvx.jpg'
map_loa = 'http://i.imgur.com/amfgSO4.jpg'
help_msg = \
"""
Доступные команды бота:

`/help` - показать это сообщение

*[Ублюдки]*
`/who` _nick_ - показать ублюдка
`/showall` - показать всех ублюдков
`/add` _nick описание_ - добавить ублюдка в список
`/del` _nick_ - удалить ублюдка из списка

*[Эксп]*
`/lvl` _уровень с процентом_ - показывает сколько опыта осталось до lvl-up
`/exp` _start end_ - таблица опыта в выбранном диапазоне лвл-ов.

*[Остальное]*
`/nickname` - поиск ника по l2on
`/quote` - цитаты великих людей
`/maploa` - карта LoA
"""

def handle(msg):
    pprint(msg)
    flavor = telepot.flavor(msg)
    chat_id = msg['chat']['id']

    if chat_id not in TRUSTED:
        bot.sendMessage(chat_id, 'Пiшов нахуй!')
        return

    command = msg['text'].split()
    sender = msg['from']['first_name']
    cmd = command[0]
    args = command[0::]

    try:
        if cmd == '/help':
            bot.sendMessage(chat_id, help_msg, parse_mode='Markdown')
        elif cmd == '/whoisyourdaddy':
            bot.sendPhoto(chat_id, daddy, disable_notification=True)
        elif cmd == '/maploa':
            bot.sendPhoto(chat_id, map_loa, disable_notification=True)
        elif cmd == '/who':
            output = ublydok.get_data(args[1])
            bot.sendMessage(chat_id, output, disable_notification=True)
        elif cmd == '/showall':
            output = ublydok.get_data_all()
            bot.sendMessage(chat_id, output, disable_notification=True)
        elif cmd == '/add':
            name = command[1]
            descr = ' '.join(command[2:])
            output = ublydok.add_data(name, descr)
            bot.sendMessage(chat_id, output, disable_notification=True)
        elif cmd == '/del':
            output = ublydok.delete_data(args[1])
            bot.sendMessage(chat_id, output, disable_notification=True)
        elif cmd == '/lvl':
            lvl = args[1]

            if len(command) == 3:
                percent = args[2].strip('%')
            else:
                percent = None

            output = sender + ', ' + ublydok.calculate_exp(lvl, percent)
            bot.sendMessage(chat_id, output, disable_notification=True)
        elif cmd == '/exp':
            try:
                x = args[1]
            except IndexError:
                x = 0
            try:
                y = args[2]
            except IndexError:
                y = 81

            output = ublydok.exp_table(x, y)
            bot.sendMessage(chat_id, output, parse_mode='Markdown', disable_notification=True)
        elif cmd == '/quote':
            output = str(ublydok.quote())
            bot.sendMessage(chat_id, output, disable_notification=True)
        else:
            cmd = cmd.strip('/ ')
            output = l2onparser.parse(cmd)
            bot.sendMessage(chat_id, output, parse_mode='Markdown', disable_web_page_preview=True, disable_notification=True)
    except IndexError:
        return None


bot.message_loop(handle)
print("Connecting to telegram servers...")
pprint(bot.getMe())

while 1:
    time.sleep(10)