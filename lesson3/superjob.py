# -*- coding: utf8 -*-
from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re
from pymongo import MongoClient

job_name = 'python'
link_hh = 'https://novosibirsk.hh.ru'
link_sj = 'https://www.superjob.ru'
header = {'Accept': '*/*',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'
          }


def get_sj_vac(link, header, job_name):
    data = list()
    link_sj = link + '/vacancy/search/?keywords=' + job_name + "&geo%5Bt%5D%5B0%5D=4"
    session = requests.session()
    re_vac = re.compile('i.*')
    re_vac_name = re.compile('icMQ_ _1QIBo .*')
    re_salary = re.compile('.*f-test-text-company-item-salary.*')
    re_delW = re.compile(r'[^0-9]')
    for page in range(1, 100):
        print(link_sj + f"&page={page}")
        response = session.get(link_sj + f"&page={page}", headers=header)
        if response.ok:
            html = bs(response.text, 'lxml')
            vac_list = html.find('div', {'id': "app"})
            vac_list = vac_list.find('div', {'style': "display:block"})

            if not vac_list:
                break

            vac_list = vac_list.findChildren('div', {'class': re_vac}, recursive=False)

            for vac in vac_list:

                vac_name = vac.find('a', {'class': re_vac_name})
                if vac_name:
                    vac_data = {}
                    vac_data['site'] = link
                    vac_data['job_name'] = vac_name.text
                    vac_data['href'] = link + vac_name['href']
                    vac_data['_id'] = link + vac_name['href']
                    vac_sal = vac.find('span', {'class': re_salary})
                    if vac_sal:
                        sal_ = str(vac_sal.text).replace('\xa0', ' ')
                        sal_min = '0'
                        sal_max = '0'

                        if sal_ == 'По договорённости':
                            sal_min = 0
                        elif sal_.count('—') > 0:
                            sal_min = sal_.split('—')[0]
                            sal_max = sal_.split('—')[1]
                        elif sal_.count('от') > 0:
                            sal_min = sal_

                        sal_max = re.sub(re_delW, '', str(sal_max))
                        sal_min = re.sub(re_delW, '', str(sal_min))
                        vac_data['salary_min'] = int(sal_min)
                        vac_data['salary_max'] = int(sal_max)

                    data.append(vac_data)

        else:
            break;

    return data


def get_hh_vac(link, header, job_name):
    data = list()
    link_hh = link + '/search/vacancy?L_is_autosearch=false&area=1&clusters=true&enable_snippets=true&text=' + job_name
    session = requests.session()
    re_vac = re.compile('vacancy-serp.*')
    re_delW = re.compile(r'[^0-9]')
    for page in range(0, 10):
        print(link_hh + f"&page={page}")
        response = session.get(link_hh + f"&page={page}", headers=header)
        if response.ok:
            html = bs(response.text, 'lxml')
            vac_head = html.find('div', {'class': 'vacancy-serp'})
            vac_l = vac_head.findChildren('div', {'class': re_vac}, recursive=False)

            for vac in vac_l:
                vac_data = {}

                vac_name = vac.find('div', {'class': 'vacancy-serp-item__info'})
                vac_name = vac_name.find('a')
                vac_data['job_name'] = vac_name.text
                vac_data['href'] = vac_name['href']
                vac_data['_id'] = vac_name['href']

                if vac_name['href']:
                    vac_data['site'] = link

                vac_sal = vac.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
                if vac_sal:
                    sal_ = vac_sal.text.replace(' ', '').replace(' ', '')
                    # print(sal_)
                    sal_min = 0
                    sal_max = 0

                    if sal_.count('-') > 0:
                        sal_min = sal_.split('-')[0]
                        sal_max = sal_.split('-')[1]

                    elif sal_.count('от') > 0:
                        sal_min = sal_  # sal_min.replace('руб.', '').replace('USD', '')

                    sal_max = re.sub(re_delW, '', str(sal_max))
                    sal_min = re.sub(re_delW, '', str(sal_min))

                    if sal_.count('USD') != 0:
                        sal_min = int(sal_min) * 75

                    vac_data['salary_min'] = int(sal_min)
                    vac_data['salary_max'] = int(sal_max)

                data.append(vac_data)


        else:
            break
    return data


# Функция записи в базу
def toDb(result):
    client = MongoClient('localhost', 27017)
    db = client['database_job']
    jobs = db.jobs1

    for res in result:
        # Удаляем предыдущие данные если они есть, ид - ссыылка на вакансию
        jobs.delete_one({'_id': res['href']})
        jobs.insert_one(res)


# поиск вакансии с ЗП более заданной
def findVac(minSal):
    client = MongoClient('localhost', 27017)
    db = client['database_job']
    jobs = db.jobs1
    cnt = 0
    print('вакансии с зарплатой боллее=', minSal)
    for job in jobs.find({'salary_min': {'$gt': minSal}}):
        pprint(job)
        cnt += 1

    print('\n вакансий=', cnt)


# MAIN
result = list()
result = result + (get_sj_vac(link_sj, header, job_name))
result = result + get_hh_vac(link_hh, header, job_name)

# Запись в базу
toDb(result)

# Поиск вакансий
findVac(200000)
