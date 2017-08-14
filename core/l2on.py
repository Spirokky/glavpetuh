from selenium import webdriver
from bs4 import BeautifulSoup

import re
import string
import requests
import config


driver = webdriver.PhantomJS(executable_path=config.webdriver_path)
URL = 'http://l2on.net'


def clean_data(dct):
    cleaned = {}
    for k, v in dct.items():
        cleaned[k] = re.sub('\\n', '', v)
    return cleaned


class Player(object):

    def __init__(self, nickname):
        self.nickname = nickname
        self.values = {
            'setworld': 1092,
            'c': 'userdata',
            'a': 'search',
            'type': 'char',
        }
        self.output = \
            """
            [{}]({})
            _{}_
            [{}]({})
            Раса: {}
            Класс: {}
            Макс. HP: `{}`
            Макс. MP: `{}`
            Клан: {}
            Альянс: {}
            Замечен: {}
            Обновлен: {}
            Торговля: {}
            """

    def nickname_validator(self):
        for char in self.nickname:
            if char in string.punctuation + string.whitespace:
                return 1

        pattern = re.compile('[а-яА-ЯёЁ]')
        match = re.search(pattern, self.nickname)

        if match:
            return 2
        else:
            return 3

    def parser(self):
        valid = self.nickname_validator()

        if valid == 1:
            return 'Невалидное имя'
        elif valid == 2:
            name = self.nickname.encode('windows-1251')
        else:
            name = self.nickname

        self.values['name'] = name

        req = requests.get(URL, params=self.values)
        soup = BeautifulSoup(req.text, 'html.parser')
        table = soup.find_all('a', 'black', href=re.compile('id'))
        players = table[::2]

        player_url = None

        for i in players:
            if i.text.lower() == self.nickname.lower():
                m = re.search('id=[0-9]+', str(i))
                start = m.span()[0]
                end = m.span()[1]
                player_id = str(i)[start:end]
                player_url = 'http://l2on.net/?c=userdata&a=char&' + player_id
                break

        if not player_url:
            return 'Ничего не найдено'

        driver.get(player_url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        char_head = soup.find_all('table', 'char-head')[0]
        player_header = char_head.find_all('h1')[0]
        player_name = player_header.contents[0]  # name
        player_comments = player_header.find_all('a')[0]
        player_comments_link = player_comments.attrs['href']  # comments url
        player_comments_string = player_comments.string  # comment's url text
        player_values = soup.find_all('table', 'values')[0]
        player_values_dict = {}

        for tag in player_values.tbody:
            try:
                player_values_dict[tag.th.string] = tag.td.text
            except AttributeError:
                pass

        pvd = clean_data(player_values_dict)  # dict of cleaned values

        output = self.output.format(player_name,
                                    player_url,
                                    pvd['Уровень'],
                                    player_comments_string,
                                    player_comments_link,
                                    pvd.get('Раса', 'None'),
                                    pvd.get('Класс', 'None'),
                                    pvd.get('Макс. HP', 'None'),
                                    pvd.get('Макс. MP', 'None'),
                                    pvd.get('Клан', 'Без клана'),
                                    pvd.get('Альянс', 'Без альянса'),
                                    pvd.get('Замечен', 'Не замечен'),
                                    pvd.get('Обновлён', 'Не обновлен'),
                                    pvd.get('Торговля', 'Не торговал'),
                                    )
        return output


if __name__ == '__main__':
    player = Player('Einsam')
    print(player.parser())
