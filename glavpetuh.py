import ublydok
import telepot
import sys
import time
import l2onparser

from pprint import pprint

TOKEN = sys.argv[1]
TRUSTED = [-188672102, # testdebug
            303422193, # Spirokky's private
           -167715634, # back to l2
            123456789]

bot = telepot.Bot(TOKEN)

daddy = 'http://i.imgur.com/b8XZVvx.jpg'
help_msg = \
"""
/who <nickname> - показать инфу об ублюдке
/add <nickname> <описание> - добавить ублюдка
/del <nickname> - убрать ублюдка
/lvl <lvl> <процент> - опыт до повышения уровня
"""

def handle(msg):
    pprint(msg)
    flavor = telepot.flavor(msg)
    chat_id = msg['chat']['id']

    if chat_id not in TRUSTED:
        bot.sendMessage(chat_id, 'Недостаточно прав')

    command = msg['text'].split()
    sender  = msg['from']['first_name']
    cmd     = command[0]
    args    = command[0::]

    try:
        if cmd == '/help':
            bot.sendMessage(chat_id, help_msg)
        elif cmd == '/whoisyourdaddy':
            bot.sendPhoto(chat_id, daddy)
        elif cmd == '/who':
            output = ublydok.get_data(args[1])
            bot.sendMessage(chat_id, output)
        elif cmd == '/add':
            name   = command[1]
            descr  = ' '.join(command[2:])
            output = ublydok.add_data(name, descr)
            bot.sendMessage(chat_id, output)
        elif cmd == '/del':
            output = ublydok.delete_data(args[1])
            bot.sendMessage(chat_id, output)
        elif cmd == '/lvl':
            lvl = args[1]

            if len(command) == 3:
                percent = args[2].strip('%')
            else:
                percent = None

            output = sender + ', ' + ublydok.calculate_exp(lvl, percent)
            bot.sendMessage(chat_id, output)
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
            bot.sendMessage(chat_id, output)
        elif cmd == '/quote':
            output = str(ublydok.quote())
            bot.sendMessage(chat_id, output)
        else:
            cmd = cmd.strip('/ ')
            output = l2onparser.parse(cmd)
            bot.sendMessage(chat_id, output)
    except IndexError:
        return None

bot.message_loop(handle)
pprint(bot.getMe())

while 1:
    time.sleep(10)