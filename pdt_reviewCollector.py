#importing required modules
import streamlit as st
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import pandas as pd
import time




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
def scrapper(product,nos):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1440, 900")
    #chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    browser.implicitly_wait(5)
    
    browser.delete_all_cookies()
    
    browser.get('https://www.amazon.com')
    
    time.sleep(8)
    browser.minimize_window()
    
    
    
    # print(browser.page_source)

    # browser.implicitly_wait(5)

    # element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'twotabsearchtextbox')))

    search_box = browser.find_element(By.ID, 'twotabsearchtextbox')

    search_box.send_keys(product)

    search_box.send_keys(Keys.ENTER)

    # browser.implicitly_wait(3)

    list_of_product_links = browser.find_elements(By.TAG_NAME, "a")

    lis = []

    for i in list_of_product_links:
        if '#customerReviews' in str(i.get_attribute('href')):
            lis.append(i.get_attribute('href'))

    tec = list(set(lis))

    # len(tec)

    product = []
    reviews = []
    prize = []
    image= []
    urlink=[]
    data_string = ""
    for url in tec[0:nos]:
        urlink.append(url)
    
    
    
    
    
    for url in tec[0:nos]:
        browser.get(url)
        
        # browser.implicitly_wait(2)
        soup = BeautifulSoup(browser.page_source, 'html.parser')

        for item in soup.find_all("span", {"data-hook": "review-body"}):
            
            drop_down = Select(browser.find_element(By.ID, 'cm-cr-sort-dropdown'))
            drop_down.select_by_value("recent")
            data_string = data_string + item.get_text()
            reviews.append(data_string.replace('\n', ''))
            data_string = ""
            product.append(soup.find("span", id="productTitle").get_text())
            try:
                prize.append(soup.find("span",class_='a-price-whole').get_text())
    
            except AttributeError :
                prize.append('NA')
            image.append(soup.find("img",class_='a-dynamic-image')['src'])

    reviews[0].replace('\n', '')

    
    data = pd.DataFrame()
#fields being printed in the streamlit interface
    data['product'] = product
    data['reviews'] = reviews
    data['prize']= prize
    data['image']= image
    
    
    
     
    browser.delete_all_cookies()
    browser.close()
    
    print(data.head(25))
    return(data,urlink)

