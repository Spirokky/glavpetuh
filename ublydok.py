import json
import sys
import os
import time
import shutil
import config
import random

current_time = time.strftime('%H%M%S')
current_date = time.strftime('%Y-%m-%d')
target_dir = 'backup' + os.sep + current_date

DB = 'blacklist.json'


def get_data(nickname):
    name = nickname.lower()

    with open(DB, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
        try:
            data = json_data[name]
        except KeyError:
            return '%s - нет в списке' % nickname

        nname = data['nickname']
        descr = data['description']
        if descr:
            res = "{} - {}".format(nname, descr)
        else:
            res = '%s - нет описания' % nname
        return res


def get_data_all():
    with open(DB, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
        values = json_data.values()
        nicknames = [v.get('nickname') for v in values]
        names_list = ''

        for i in sorted(nicknames):
            names_list += i + '\n'

    return names_list



def backup(fname):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    with open(fname, 'rb') as f:
        filename = current_time + '.json'
        shutil.copy(fname, os.path.join(target_dir, filename))

    return None


def add_data(nickname, info=None):
    name = nickname.lower()

    with open(DB, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

        if name in json_data.keys():
            return '%s уже есть в списке' % nickname

        json_data[name] = {'nickname': nickname, 'description': info}

    backup(DB)

    with open(DB, 'w') as f:
        json.dump(json_data, f)
        return '%s добавлен в список' % nickname


def delete_data(nickname):
    name = nickname.lower()

    with open(DB, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

        if name not in json_data.keys():
            return '%s нет в списке' % nickname
        else:
            json_data.__delitem__(name)

    backup(DB)

    with open(DB, 'w') as f:
        json.dump(json_data, f)
        return '%s убран из списка' % nickname


def calculate_exp(lvl, percent=None):
    nextlvl = str(int(lvl) + 1)
    total_exp = config.levels[lvl][0]

    if percent:
        x = 100 - float(percent)
        need_exp = round(int(config.levels[nextlvl][1]) * x / 100)
    else:
        need_exp = config.levels[nextlvl][1]

    output = 'Опыта до lvl-up: {:,}'
    return output.format(need_exp)


def exp_table(x=0, y=81):
    x, y = int(x), int(y)
    rng = range(x, y + 1)
    output = ' *{:>3}  {:^18}  {:^18}*\n'.format('lvl', 
                                                'До повышения', 
                                                'Всего опыта')
    table = config.levels   

    for i in rng:
        for k, v in table.items():
            if k == str(i):
                output += '{:>3} | {:^18,} | {:^18,}\n'.format(i, v[1], v[0])

    return output


def quote():
    t = time.time()
    random.seed(t)
    lst = config.quotes
    arr_len = len(lst) - 1
    i = random.randint(0, arr_len)
    return lst[i]


if __name__ == '__main__':
    pass
