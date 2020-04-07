from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

chrome_options = Options()
webdriver.chrome
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.get('https://www.mvideo.ru/')
pages = 0

#//div[@class='gallery-layout sel-hits-block ']
#//a[@class='next-btn sel-hits-button-next']

elem = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//div[@class="gallery-layout sel-hits-block "]'))
)

elems = driver.find_elements_by_xpath('//div[@class="gallery-layout sel-hits-block "]')

hits= driver.find_element_by_xpath('//div[@class="gallery-layout sel-hits-block "]')


res_data=list()
while True:
    try:
        elem = hits.find_element_by_xpath('.//a[@class="next-btn sel-hits-button-next"]')
        btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@class="next-btn sel-hits-button-next"]')))
        elems = hits.find_elements_by_xpath('.//li[@class="gallery-list-item"]')

        # for it in elems:
        #     data={}
        #     data['price']=it.find_element_by_xpath('.//div[@class="c-pdp-price__current"]').text
        #     res_data.append(data)
        elem.click()
        sleep(5)
    except Exception as e:
        break
        print('выход ',e)


