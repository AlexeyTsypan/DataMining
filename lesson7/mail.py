import scrapy
from mail.items import MailItem
from scrapy.loader import ItemLoader

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


class SpmailSpider(scrapy.Spider):
    name = 'SpMail'
    allowed_domains = ['e.mail.ru']
    start_urls = ['https://e.mail.ru/inbox']

    def parse(self, response):
        chrome_options = Options()
        webdriver.chrome
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://e.mail.ru/inbox')

        elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'Login'))
        )
        elem.send_keys('study.ai_172@mail.ru')

        elem = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-test-id="next-button"]'))
        )
        elem.click()

        elem = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@name="Password"]'))
        )
        elem.send_keys('NewPassword172')

        elem = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-test-id="submit-button"]'))
        )

        elem.click()

        elem = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="dataset__items"]'))
        )

        letters_temp = driver.find_elements_by_xpath('//a[contains(@class, "js-letter")]')
        letters = list()


        while True:
            tst = 0
            for it in letters_temp:
                hr = it.get_attribute('href')
                if letters.count(hr) > 0:
                    tst += 1
                else:
                    letters.append(hr)
                    loader = ItemLoader(item=MailItem(), response=response)
                    loader.add_value('name', it.find_element_by_xpath('//span[contains(@class, "ll-sj__normal")]').text)
                    loader.add_value('href', hr)
                    yield loader.load_item()

            if tst == len(letters_temp):
                break

            last = driver.find_element_by_xpath('//a[contains(@class, "js-letter")][last()]')
            last.send_keys(Keys.CONTROL + Keys.END)
            letters_temp = driver.find_elements_by_xpath('//a[contains(@class, "js-letter")]')
