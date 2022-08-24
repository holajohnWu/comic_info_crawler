import requests as rq
from bs4 import BeautifulSoup
import time
from datetime import datetime
from os.path import exists
import os


def sleeptime(hour, min, sec):
    return hour*3600 + min*60 + sec


def crawComicInfo(urls):
    result = []
    for url in urls:
        print('start craw:' + url)
        resp = rq.get(url)
        soup = BeautifulSoup(resp.text, "html.parser")
        img = soup.find('p', class_='hcover').select_one('img')
        imgHref = img.get('src')
        comicName = soup.find('div', class_='book-title').find('h1').getText()
        status = soup.find('li', class_='status').find('span')
        lastUpdateTime = status.select('span')[1].getText()
        newestChapter = status.find('a').getText()
        result.append({'name': comicName, 'last_update': lastUpdateTime,
                       'chapter': newestChapter, 'img': imgHref})
        print('finish')
        time.sleep(sleeptime(0, 0, 5))
    return result
