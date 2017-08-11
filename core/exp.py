import config


class Exp(object):

    LEVELS = config.levels

    def __init__(self):
        pass

    def next_level(self, lvl, percent=None):
        nextlvl = str(int(lvl) + 1)

        if percent:
            x = 100 - float(percent)
            res = round(int(config.levels[nextlvl][1]) * x / 100)
        else:
            res = config.levels[nextlvl][1]

        output = 'Опыта до lvl-up: {:,}'
        return output.format(res)

    def exp_table(self, start=1, end=85):
        pass


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

if __name__ == "__main__":
    exp = Exp()
    print(exp.next_level(23, 50))
    print(exp.next_level(23))
    print(exp.next_level(0))