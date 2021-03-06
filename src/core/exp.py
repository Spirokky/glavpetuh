import requests
import yaml
import re

from bs4 import BeautifulSoup
from datetime import datetime


with open('config.yaml', 'r') as f:
    cfg = yaml.load(f)


class Exp(object):

    def __init__(self):
        self.levels = cfg['levels']

    def next_level(self, lvl, percent=None):
        lvl = int(lvl)

        if lvl <= 0:
            return "Минимальный уровень: 1"

        if lvl > 85:
            return 'Максимальный уровень: 85'

        if lvl == 85:
            nextlvl = 85
        else:
            nextlvl = lvl + 1

        if percent:
            percent = float(percent)
            if percent > 100:
                return 'Больной ублюдок'
            else:
                x = 100 - percent
                res = round(self.levels[nextlvl][1] * x / 100)
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
                if k == i:
                    output += '{:>3} | {:<16,} | {:<16,}\n'.format(i, v[1],
                                                                   v[0])
        output += "```"
        return output

    def get_stats_today(self):
        urls = cfg['L2tracker']
        result = []

        for url in urls:
            req = requests.get(url)
            soup = BeautifulSoup(req.text, 'html.parser')
            name = soup.find('a', {'href': re.compile('\?char_id=*')}).string
            lvl = soup.caption.string.split()[0]
            first_row = soup.find('tr', {'class': 'level' + str(lvl)})

            if first_row:
                date = first_row.find_all('td')[0].string

                today = datetime.now()

                if today.strftime('%Y-%m-%d') != date:
                    continue

                exp_data = []
                for string in first_row.find_all('td')[2].strings:
                    exp_data.append(string)

                try:
                    total_exp = exp_data[0].replace(' ', '')
                except IndexError:
                    total_exp = '0'

                try:
                    exp_gained = exp_data[3].replace(' ', '')
                except IndexError:
                    exp_gained = '+0'

                percents = []
                for string in first_row.find_all('td')[3].stripped_strings:
                    percents.append(string.rstrip('(), '))

                try:
                    total_percent = percents[0]
                except IndexError:
                    total_percent = '0'

                try:
                    percent_gained = percents[1]
                except IndexError:
                    percent_gained = '+0%'

                pvp = []
                for string in first_row.find_all('td')[4].stripped_strings:
                    pvp.append(string.rstrip('() '))

                try:
                    total_pvp = pvp[0].replace(' ', '')
                except IndexError:
                    total_pvp = "0"

                try:
                    pvp_gained = pvp[1].replace(' ', '')
                except IndexError:
                    pvp_gained = "+0"

                pk = []
                for string in first_row.find_all('td')[5].stripped_strings:
                    pk.append(string.rstrip('() '))

                try:
                    total_pk = pk[0].replace(' ', '')
                except IndexError:
                    total_pk = "0"

                try:
                    pk_gained = pk[1].replace(' ', '')
                except IndexError:
                    pk_gained = "+0"

                res = [name, date, lvl, total_exp, exp_gained,
                       total_percent, percent_gained, total_pvp,
                       pvp_gained, total_pk, pk_gained]

                result.append(res)
            else:
                continue

        return result


if __name__ == "__main__":
    pass
