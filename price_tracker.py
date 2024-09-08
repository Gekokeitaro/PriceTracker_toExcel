# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 15:27:28 2024

@author: pablo
"""

from bs4 import BeautifulSoup
import requests as r
import os
import json

import time
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

HEADERS : dict = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
    }

PRODUCTS_JSONS = './Products_JSONs/'

def read_json(json_path : str) -> dict:
    print(json_path)
    with open(json_path, 'r') as file:
        return json.load(file)

def getWebHtml(driver, product_url : str, actions=[]) -> str:
    
    time.sleep(5)
    
    #Vamos a la página indicada pccomponentes.com/laptops
    driver.get(product_url)
    
    #Esperamos 30 segundos hasta que aparezca el botón de cookies y al aparecer hace clic
    #if 'click_cookies' in actions:
     #   accept_cookies = WebDriverWait(driver, 30).until(
      #      EC.presence_of_element_located((By.ID, actions['click_cookies']))
       # )     
        
        #accept_cookies.click()
        
    #Descargamos el HTML
    html = driver.page_source
            
    if html:
        return BeautifulSoup(html, 'html.parser')
    else :
        print(f"Failed to fetch content from {product_url}:")
        return None
    
def priceToInt(priceStr : str) -> int:
    priceTmp = priceStr.strip().replace("€", "").replace(",",".")
    
    return int(float(priceTmp)) if len(priceTmp.rsplit(".")[0]) > 2 else int(float(".".join(priceTmp.rsplit(".")[:-1])))
    

def main() -> None:
    # Selenium
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install() ,options=options)

    try:
        product_lst = [file for file in os.listdir(PRODUCTS_JSONS) if file.endswith('.json') and not file.startswith('NO_')]
    
        for product_dict in product_lst:
            
            product_data = read_json(os.path.join(PRODUCTS_JSONS, product_dict))
            base_url = product_data['base_url']
            base_suffix = product_data['suffix'] if 'suffix' in product_data else None
            
            for product in product_data['products']:
    
                product_url = '/'.join([base_url, base_suffix, product]) if base_suffix else '/'.join([base_url, product])
                soup = getWebHtml(driver, product_url, product_data['actions'])
                
                if not soup: continue
            
                search_params = dict(product_data['find'])
                price = soup.find(search_params['tag'], attrs=search_params['attr'])
                 
                # Si el valor del precio se encuentra en una propiedad HTML...
                if 'property_w_value' in product_data:
                    html_property = product_data['property_w_value']
                    print(f"{int(float(price[html_property].strip()))}")
                else:
                    print(priceToInt(price.text))
                    
                    #print(f"{float(price['content']):.2f}")
    finally:
       driver.quit()

if __name__ == '__main__':
    main()