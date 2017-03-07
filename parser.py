import re
import string
import urllib.request
import urllib.parse
import requests

from urllib.parse import quote_from_bytes as qfb
from pprint import pprint
from bs4 import BeautifulSoup

url = 'http://l2on.net'


def is_valid(nickname):

    """
    returns 0 if nickname is invalid
    returns 1 if nickname is cyrillic
    returns 2 if nickname is valid
    """

    for char in nickname:
        if char in string.punctuation + string.whitespace:
            return 0

    pattern = re.compile('[а-яА-ЯёЁ]')
    match = re.search(pattern, nickname)

    if match:
        return 1

def parser(nickname):
    valid = is_valid(nickname)
    
    if valid == 0:
        return 'Невалидное имя'
    elif valid == 1:
        name = nickname.encode('windows-1251')
    else:
        name = nickname

    values = {'setworld': 1092,
              'c': 'userdata',
              'a': 'search',
              'type': 'char',
              'name': name}

    req     = requests.get(url, params=values)
    soup    = BeautifulSoup(req.text, 'html.parser')
    table   = soup.find_all('a', 'black', href=re.compile('id'))
    players = table[::2]

    for i in players:
        if i.text.lower() == nickname.lower():
            m          = re.search('id=[0-9]+', str(i))
            start      = m.span()[0]
            end        = m.span()[1]
            player_id  = str(i)[start:end]
            player_url = 'http://l2on.net/?c=userdata&a=char&' + player_id
            break
        else:
            player_url = None
    
    if not player_url:
        print('Ничего не найдено')
    else:
        print(player_url)

while 1:
    parser(input('name: '))
