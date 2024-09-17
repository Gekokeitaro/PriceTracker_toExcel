# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 22:47:50 2024

@author: pablo
"""

import requests
from bs4 import BeautifulSoup
import random
import time
import os
import json

CONFIG_PATH = r'./proxy_rotator_config'
CONFIG_FILE = os.path.join(CONFIG_PATH,'config.json')
PROXIES_FILE = os.path.join(CONFIG_PATH,'proxies_list.json')
WORKING_PROXIES_FILE = os.path.join(CONFIG_PATH,'working_proxies_list.json')

PROXY_MAX_RETRIES = 3
PROXY_TIMEOUT = 5

REQUEST_MAX_RETRIES = 3

def get_proxies_by_region():
    # working_proxies_lst = None
    
    # if os.exist(WORKING_PROXIES_FILE):
    #     working_proxies_lst = get_proxies_from_file(WORKING_PROXIES_FILE)
    
    region, country = get_ip_region_country()
    
def get_ip_region_country(working_proxies : list = None):
    
    try:
        response = requests.get("https://ipinfo.io")
        data = response.json()
        return data.get('region'), data.get('country')
    except requests.RequestException as e:
        print(f'error encontrando la región y país: {e}')
        return None
    
def get_proxies_from_file(json_path : str) -> list:
    try:
        with open(json_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f'Error leyendo {json_path}: {e}')
        return None
    