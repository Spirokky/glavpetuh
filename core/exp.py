import config


def calculate_exp(lvl, percent=None):
    nextlvl = str(int(lvl) + 1)

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
