import re
import os
import string
import logging
import numpy as np
import six
import matplotlib
import yaml
import logging.config

matplotlib.use('Agg')
import matplotlib.pyplot as plt

from datetime import datetime

logger = logging.getLogger('')


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


def setup_logging(default_path='logging.yaml',
                  default_level=logging.INFO,
                  env_key='LOG_CFG'):
    """
    Setup logging configuration
    """

    if 'logs' not in os.listdir():
        os.mkdir('logs')

    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


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
            logger.info("Create directory /statistics")

        filename = "statistics/{}.png".format(now)
        logger.info("Saving file %s" % filename)
        plt.savefig(filename)
        logger.info("File saved")
        return filename
    except Exception as e:
        logger.error("Something went wrong: %s" % e)
        return None


setup_logging()

if __name__ == '__main__':
    pass
