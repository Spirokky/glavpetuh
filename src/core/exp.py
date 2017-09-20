import requests
import numpy as np
import matplotlib.pyplot as plt
import six

from config import config, secrets
from bs4 import BeautifulSoup
from datetime import datetime


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

            if first_row:
                date = first_row.find_all('td')[0].string

                today = datetime.datetime.now()

                if today.strftime('%Y-%m-%d') != date:
                    continue

                exp_data = []
                for string in first_row.find_all('td')[2].strings:
                    exp_data.append(string)

                try:
                    total_exp = exp_data[0].replace(' ', '')
                except IndexError:
                    total_exp = None

                try:
                    exp_gained = exp_data[3].replace(' ', '')
                except IndexError:
                    exp_gained = None


                percents = []
                for string in first_row.find_all('td')[3].stripped_strings:
                    percents.append(string.rstrip('(), '))

                try:
                    total_percent = percents[0]
                except IndexError:
                    total_percent = None

                try:
                    percent_gained = percents[1]
                except IndexError:
                    percent_gained = None


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


def render_mpl_table(data, col_width=1.0, row_height=0.625, font_size=12,
                     header_color='#40466e', row_colors=['#f7f7f7', 'w'],
                     edge_color='w', bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):

    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        fig.subplots_adjust(left=0, bottom=0, right=1, top=1)
        ax.axis('off')

    mpl_table = ax.table(cellText=data.values, cellLoc="center", bbox=bbox, colLabels=data.columns, **kwargs)

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in six.iteritems(mpl_table._cells):
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0]%len(row_colors)])

    try:
        now = datetime.now().strftime("%Y-%m-%d")
        filename = "{}-stats.png".format(now)
        plt.savefig(filename)
        return filename
    except Exception:
        return None


if __name__ == "__main__":
    pass