import math
import requests
from bs4 import BeautifulSoup
import json
import time
import random
import numpy as np
import os

from dotenv import load_dotenv

load_dotenv()
sw_username = os.getenv("sw_username")
sw_password = os.getenv("sw_password")

from six.moves import cPickle as pickle
import six

with open("man_vs_woman_suffixes", 'rb') as f:
    suf = pickle.load(f)

def _get_matching_suffix(name, suffixes):
    # it is important(!) to try suffixes from longest to shortest
    for suffix_length in six.moves.xrange(len(name), 0, -1):
        suffix = name[-suffix_length:]
        if suffix in suffixes:
            return (suffix, suffixes[suffix])
    return ('', suffixes.get(''))

def sex(name):
    name = six.text_type(name).lower()
    return _get_matching_suffix(name, suf)[1] or 'm'


def getNames(url):
    response = session.get('https://www.utvs.cvut.cz/'+url)

    soup = BeautifulSoup(response.content, "html.parser")
    bar = soup.find("table", {"class": "sp-ptbl darkrow"})
    if bar is None:
        return 'Nikdo lol'
    names = bar.find_all("tr", {})[1:]

    res = [name.text[1:-1].replace('\n', ' ') for name in names]
    return res

with requests.session() as session:
    response = session.get('https://www.utvs.cvut.cz/vyuka/seznam-studentu-2?#lerr')

    login = {
        "authtype": "cvut",
        "sw_username": sw_username,
        "sw_password": sw_password,
        "submit": ""
    }

    r_post = session.post('https://www.utvs.cvut.cz/prihlaseni', data=login)

    response = session.get('https://www.utvs.cvut.cz/vyuka/povinna-volitelna?s%5B%5D=1&s%5B%5D=2&s%5B%5D=33&s%5B%5D=3&s%5B%5D=4&s%5B%5D=125&s%5B%5D=118&s%5B%5D=5&s%5B%5D=124&s%5B%5D=32&s%5B%5D=115&s%5B%5D=121&s%5B%5D=107&s%5B%5D=7&s%5B%5D=9&s%5B%5D=10&s%5B%5D=109&s%5B%5D=11&s%5B%5D=106&s%5B%5D=120&s%5B%5D=108&s%5B%5D=12&s%5B%5D=119&s%5B%5D=128&s%5B%5D=15&s%5B%5D=112&s%5B%5D=16&s%5B%5D=17&s%5B%5D=18&s%5B%5D=19&s%5B%5D=123&s%5B%5D=29&s%5B%5D=105&s%5B%5D=100&s%5B%5D=20&s%5B%5D=34&s%5B%5D=127&s%5B%5D=114&s%5B%5D=21&s%5B%5D=31&s%5B%5D=22&s%5B%5D=24&s%5B%5D=25&s%5B%5D=26&s%5B%5D=129&s%5B%5D=27&s%5B%5D=28&d=0&t=420%3B1380')

    soup = BeautifulSoup(response.content, "html.parser")
    bar = soup.find("table", {"class": "expandable darkrowexp"})
    builder = ''
    data = []
    for line in bar.contents:
        if line != '\n' and line.name == 'tr':
            if len(line.attrs) == 0:
                sport = line.contents[3].text
                day = line.contents[5].text
                time = line.contents[7].text
                place = line.contents[11].text
                teacher = line.contents[13].text

                # print(line.contents[3].text)
            elif line.attrs['class'][0] == 'expansion':
                names = getNames(line.contents[1].contents[12].attrs['href'])
                m = 0
                f = 0
                for name in names:
                    if sex(name) == 'm':
                        m += 1
                    else:
                        f += 1
                ratio = f/(m+f)
                print(sport, day, time, place, teacher, ratio, names)
                builder += f'{sport} {day} {time} {place} {teacher} {ratio} {names}\n'
                data.append([sport, day, time, place, teacher, ratio, names])

    with open('data.txt', 'w') as f:
        f.write(builder)
