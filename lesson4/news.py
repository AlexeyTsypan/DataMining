from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re
from pymongo import MongoClient
from lxml import html
import datetime

link_mail = 'https://news.mail.ru'
link_mail_reg = '/inregions/siberian/54/'

link_lenta = 'https://lenta.ru'

link_ya = 'https://yandex.ru'

header = {'Accept': '*/*',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'
          }


def getFMail(link, header, region):
    data = list()
    try:
        session = requests.session()
        response = session.get(link + region, headers=header)
        if response.ok:
            tree = html.fromstring(response.text)
            news_list = tree.xpath(
                "//a[contains(@class,'link_flex')] | //a[contains(@class,'topnews')] | //a[contains(@class,'list__text')] ")

            for n in news_list:
                n_data = {}
                n_data['source'] = link
                if n.text:
                    n_data['text'] = n.text
                elif n.xpath(".//span[@class='link__text']/text()"):
                    n_data['text'] = ''.join(n.xpath(".//span[@class='link__text']/text()")).replace(u'\xa0', '')
                else:
                    n_data['text'] = ''.join(n.xpath(".//span[@data-id]/text()")).replace(u'\xa0', '')

                n_data['href'] = link + n.xpath("@href")[0]
                n_data['date'] = ''  # datetime.date.today()
                data.append(n_data)
        return data
    except Exception as e:
        print('Err = ', e)


def getFLenta(link, header):
    data = list()
    try:
        session = requests.session()
        response = session.get(link, headers=header)
        if response.ok:
            tree = html.fromstring(response.text)
            news_list = tree.xpath(
                "//div[contains(@class,'item')]//div[@class='titles'] | //div[contains(@class,'item')]//a[contains(@href,'news')]")

            for n in news_list:
                n_data = {}

                n_data['source'] = link
                if len(n.xpath('text()')) > 0:
                    n_data['text'] = ' '.join(n.xpath('text()')).replace(u'\xa0', '')
                elif len(n.xpath('.//span/text()')) > 0:
                    n_data['text'] = n.xpath('.//span/text()')[0].replace(u'\xa0', '')

                if len(n.xpath('@href')) > 0:
                    n_data['href'] = n.xpath("@href")[0]
                elif len(n.xpath('.//a/@href')) > 0:
                    n_data['href'] = n.xpath('.//a/@href')[0]

                if len(n_data['href']) > 0 and n_data['href'].count('http') == 0:
                    n_data['href'] = link + n_data['href']

                if len(n.xpath('.//time/@datetime')) > 0:
                    n_data['date'] = str(n.xpath('.//time/@datetime')[0]).replace(' ', '')
                else:
                    n_data['date'] = ''

                data.append(n_data)

        return data
    except Exception as e:
        print('Err = ', e)


def getFMYa(link, header):
    data = list()
    session = requests.session()
    response = session.get(link + '/news', headers=header)
    if response.ok:
        tree = html.fromstring(response.text)
        news_list = tree.xpath(
            "//a[contains(@class,'link_theme_black')]")

        for n in news_list:
            n_data = {}
            n_data['source'] = link
            n_data['text'] = n.text
            n_data['href'] = link + n.xpath("@href")[0]
            n_data['date'] = ''  # datetime.date.today()
            data.append(n_data)

    return data


# Функция записи в базу
def toDb(result):
    client = MongoClient('localhost', 27017)
    db = client['database_news']
    news = db.news1
    news.delete_many({})

    news.insert_many(result)


# MAIN
result = list()

result += getFMail(link_mail, header, link_mail_reg)
result += getFLenta(link_lenta, header)
result += getFMYa(link_ya, header)

toDb(result)
