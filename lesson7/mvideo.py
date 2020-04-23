# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import json
from pymongo import MongoClient

chrome_options = Options()
webdriver.chrome
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.get('https://www.mvideo.ru/')
pages = 0

# //div[@class='gallery-layout sel-hits-block ']
# //a[@class='next-btn sel-hits-button-next']

elem = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//div[@class="gallery-layout sel-hits-block "]'))
)

elems = driver.find_elements_by_xpath('//div[@class="gallery-layout sel-hits-block "]')

hits = driver.find_element_by_xpath('//div[@class="gallery-layout sel-hits-block "]')


while True:
    try:
        elem = hits.find_element_by_xpath('.//a[@class="next-btn sel-hits-button-next"]')
        btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@class="next-btn sel-hits-button-next"]')))
        elem.click()
        time.sleep(2)
    except Exception as e:
        break
        print('выход ', e)

elems = hits.find_elements_by_xpath('.//li[@class="gallery-list-item"]')

res_data = list()
for it in elems:
    href = it.find_element_by_xpath('.//a').get_attribute('href')
    data_prod = it.find_element_by_xpath('.//a').get_attribute('data-product-info').replace('\\n\\t\\t\\t\\t\\t\\t','').replace(
        '\n','').replace('\t','').replace('\\','')
    data = json.loads(data_prod)
    data['href'] = href
    res_data.append(data)

client = MongoClient('localhost', 27017)
mongo_base = client.mvideo
collection = mongo_base['0904']
collection.insert_many(res_data)
