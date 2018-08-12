#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 14:07:32 2018

@author: Melody
"""

import time
from selenium import webdriver
import pickle, os, sys
from selenium.webdriver.chrome.options import Options

def setDriver():
    if sys.platform == 'darwin':
        type_chromedriver = "chromedriver_darwin"
    elif sys.platform == 'linux':
        type_chromedriver = "chromedriver_linux"
    elif sys.platform == 'win32':
        type_chromedriver = "chromedriver_win32.exe"
    path_chromedriver = os.path.join(os.path.dirname(os.path.realpath(__file__)), type_chromedriver)
    options = Options()
    # options.add_argument("--headless") # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox') # Bypass OS security model
    options.add_argument('--disable-gpu')  # applicable to windows os only
    options.add_argument('start-maximized') #
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(path_chromedriver, chrome_options=options)
    return driver

def get_comp_name(text):
    name = ''
    count = 0
    start = False
    stop = False
    for char in text:
        if count == 2:
            return name
        if start:
            name += char
        if char == '\n':
            start = True
            count +=1

def remove_null(comp_list):
    for comp in comp_list:
        if comp == '':
            comp_list.remove('')
    return list(set(comp_list))

def hazard_to_company(chemical,driver):
    try:
        driver.get('http://npirspublic.ceris.purdue.edu/ppis/')
        driver.find_element_by_xpath("//input[@id='ContentPlaceHolder1_active']").click()

        driver.find_element_by_xpath("//input[@id='ContentPlaceHolder1_TextBoxInput2']").send_keys(chemical)

        driver.find_element_by_xpath("//input[@type='submit']").click()
        company = driver.find_element_by_xpath("//input[@type='submit' and @value='Display Companies']")
        chem_info = {}

        company.click()
        pc_code = driver.find_element_by_xpath("//span[@style='color:Black;font-weight:bold;']").text
        chem_name = driver.find_element_by_xpath("//span[@style='color:black;font-weight:bold']").text
        num_companies = driver.find_element_by_xpath("//span[@style='color:Black;font-weight:bold']").text
        td_list = driver.find_element_by_xpath("//table[@width='100%']").find_elements_by_xpath("//td")
        #tbody_list = driver.find_element_by_xpath("//tbody")
        comp_list = []
        for td in td_list:
            if td.find_element_by_xpath("//input[@type='submit' and @value='Display Products']") != []:
                if 'Company Information' not in td.text:
                    comp_list.append(td.text)
        names = ''
        for comp in remove_null(comp_list):
            names += get_comp_name(comp)
        return remove_null(names.split('\n'))
    except:
        print('Unable to find companies for the hazard')
        return []

if __name__ == "__main__":
    # hazards: formaldehyde, glyphosate, arsenic, aluminum, carbaryl
    name = input("Please enter a hazard name: ")
    driver = setDriver()
    comp_list = hazard_to_company(name, driver)
    print(comp_list)
