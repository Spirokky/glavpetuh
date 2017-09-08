import requests

from config import config, secrets
from bs4 import BeautifulSoup
from datetime import datetime
from operator import itemgetter

class Exp(object):

    def __init__(self):
        self.levels = config.levels

    def next_level(self, lvl, percent=None):
        if int(lvl) <= 0:
            return "Минимальный уровень: 1"

        if int(lvl) > 85:
            return 'Максимальный уровень: 85'

        if int(lvl) == 85:
            nextlvl = '85'
        else:
            nextlvl = str(int(lvl) + 1)

        if percent:
            if int(percent) > 100:
                return 'Больной ублюдок'
            else:
                x = 100 - float(percent)
                res = round(int(self.levels[nextlvl][1]) * x / 100)
        else:
            res = self.levels[nextlvl][1]

        output = 'Опыта до lvl-up: {:,}'
        return output.format(res)

    def exp_table(self, start=1, end=85):
        start, end = int(start), abs(int(end))

        if start > end:
            return 'НАЧАЛО должно быть меньше КОНЦА'

        if start < 1:
            start = 1

        if end > 85:
            end = 85

        rng = range(start, end + 1)
        output = '```\n{:>3}   {:<16}   {:<16}\n'.format('lvl',
                                                     'До повышения',
                                                     'Всего опыта')
        table = self.levels

        for i in rng:
            for k, v in table.items():
                if k == str(i):
                    output += '{:>3} | {:<16,} | {:<16,}\n'.format(i, v[1],
                                                                   v[0])
        output += "```"
        return output

    def get_stats_today(self):
        urls = secrets.l2tracker
        result = []

        for name, url in urls.items():
            req = requests.get(url)
            soup = BeautifulSoup(req.text, 'html.parser')
            lvl = soup.caption.string.split()[0]
            first_row = soup.find('tr', {'class': 'level' + str(lvl)})
            cells = first_row.find_all('td')
            date = cells[0].string
            now = datetime.now().strftime('%Y-%m-%d')

            if date != now:
                continue
            try:
                exp_gained = cells[2].find_all('span')[1].string
            except IndexError:
                exp_gained = +0

            percent = cells[3].text
            pvp_count = cells[4].text
            result.insert(1, (lvl, name, exp_gained, percent, pvp_count))

        if not result:
            return None

        res = sorted(result, key=lambda tup: tup[0], reverse=True)

        return res


if __name__ == "__main__":
    exp = Exp()
    print(exp.get_stats_today())