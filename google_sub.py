#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 13:51:20 2018

@author: Melody
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
from selenium import webdriver
import pickle
from selenium.webdriver.chrome.options import Options
import json, os, re, sys, subprocess

def setDriver():
    if sys.platform == 'darwin':
        type_chromedriver = "chromedriver_darwin"
    elif sys.platform == 'linux':
        type_chromedriver = "chromedriver_linux"
    elif sys.platform == 'win32':
        type_chromedriver = "chromedriver_win32.exe"
    path_chromedriver = os.path.join(os.path.dirname(os.path.realpath(__file__)), type_chromedriver)
    options = Options()
    options.add_argument("--headless") # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox') # Bypass OS security model
    options.add_argument('--disable-gpu')  # applicable to windows os only
    options.add_argument('start-maximized') #
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(path_chromedriver, chrome_options=options)
    return driver

def get_sub(company, driver):
    try:
        query = company+"+subsidiaries"
        goog_search = "https://www.google.co.uk/search?q=" + query
        driver.get(goog_search)
        divs = driver.find_elements_by_xpath("//div[@class='kltat']")
        #links = driver.find_elements_by_xpath("//a[@class='klitem']")
    
        sub_list = []
        
        for div in divs:
            sub_list.append(div.text)
            
        return sub_list
    except:
        print("Unable to find google subsidiaries")
        return []



if __name__ == "__main__":
    name = input("Please enter a company name: ")
    driver = setDriver()
    master_dict = get_sub(name,driver)
    print(master_dict)
    
    

    
