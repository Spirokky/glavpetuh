import re
import os
import string
import logging
import numpy as np
import six
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from datetime import datetime


formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s',
                              datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger('utils')
logger.setLevel(logging.INFO)

fh = logging.FileHandler('logs/bot.log')
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(console)


def clean_data(dct):
    cleaned = {}
    for k, v in dct.items():
        cleaned[k] = re.sub('\\n', '', v)
    return cleaned


def validate_nickname(nickname):
    for char in nickname:
        if char in string.punctuation + string.whitespace:
            return 1
    pattern = re.compile('[а-яА-ЯёЁ]')
    match = re.search(pattern, nickname)
    if match:
        return 2
    else:
        return 3


def render_mpl_table(data, col_width=1.0, row_height=0.625, font_size=12,
                     header_color='#40466e', row_colors=['#f7f7f7', 'w'],
                     edge_color='w', bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array(
            [col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        fig.subplots_adjust(left=0, bottom=0, right=1, top=1)
        ax.axis('off')

    mpl_table = ax.table(cellText=data.values, cellLoc="center", bbox=bbox,
                         colLabels=data.columns, **kwargs)

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in six.iteritems(mpl_table._cells):
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0] % len(row_colors)])

    try:
        now = datetime.now().strftime("%Y-%m-%d")

        if 'statistics' not in os.listdir():
            os.mkdir('statistics')
            logger.info("Created directory /statistics")

        filename = "statistics/{}.png".format(now)
        logger.info("Saving file %s" % filename)
        plt.savefig(filename)
        logger.info("File saved")
        return filename
    except Exception as e:
        logger.error("Something went wrong: %s" % e)
        return None


if __name__ == '__main__':
    pass
