# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 16:32:34 2018

@author: Melody
"""

import time
from selenium import webdriver
import pickle
import json, os, re, sys, subprocess
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

def setDriver():
    options = Options()
    options.add_argument("--headless") # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox') # Bypass OS security model
    options.add_argument('--disable-gpu')  # applicable to windows os only
    options.add_argument('start-maximized') #
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(chrome_options=options)
    return driver

def get_sub_list(company, driver):
    query = company+"+subsidiaries"
    goog_search = "https://www.google.co.uk/search?q=" + query

    driver.get(goog_search)
    sub_list = []
    
    # find tags containing subsidiary information

    divs1 = driver.find_elements_by_xpath("//div[@class='kltat']")
    divs2 = driver.find_elements_by_xpath("//div[@class='Z0LcW']")
    divs3 = driver.find_elements_by_xpath("//div[@class='title']")
    
    # Google appears to have one of the three types of subsidiary tags
    if divs1 != []:
        for div in divs1:
            sub_list.append(div.text)
        return sub_list
    elif divs2 != []:
        for div in divs2:
            sub_list.append(div.text)
        return sub_list
    elif divs3 != []:
        for div in divs3:
            sub_list.append(div.text)
        return sub_list        
    return sub_list


def get_sub_dict(sub, sub_list):
    sub_dict = {}
    sub_dict[sub] = sub_list
    return sub_dict

# go one level down in subsidiary list
def get_list_of_dict(comp_name,driver):
    sub_list = get_sub_list(comp_name,driver)
    time.sleep(2)
    for sub in sub_list:
        sub_sub_list = get_sub_list(sub,driver)
        # if one-level-down subsidiaries are found, replace the original company name in the list with a dictionary
        # of company name to subsidiaries
        if sub_sub_list != [] and '' not in sub_sub_list:
            sub_dict = get_sub_dict(sub,sub_sub_list)
            i = sub_list.index(sub)
            sub_list[i] = sub_dict
            print(comp_name+' subsidiaries found')
        # limit rate in order not to get banned
        time.sleep(2)
    return sub_list

# go all levels down in subsidiary list
def all_level_down(list_of_dict):
    for sub in list_of_dict:
        try:
            for key in sub.keys():
                for name in sub[key]:
                    sub_list_of_dict = get_list_of_dict(name,driver)
                    if sub_list_of_dict != [] and '' not in sub_list_of_dict:
                        sub_dict = get_sub_dict(name,sub_list_of_dict)
                        i = list_of_dict.index(sub)
                        j = list_of_dict[i][key].index(name)
                        list_of_dict[i][key][j] = sub_dict
        except:
            pass
    return list_of_dict

if __name__ == "__main__":
    comp_name = input('Enter a company name: ')
    # set driver first
    driver = setDriver()
    sub_list = get_list_of_dict(comp_name,driver)
    # print result of all subsidiaries as a list
    print(all_level_down(sub_list))
    # example output:
     '''{'ABC-MART,INC.': ['ABC-Mart Korea Co,. Ltd',
  {'LaCrosse Footwear': ['Danner Inc',
    "White's Boots",
    'LaCrosse Europe ApS',
    'Environmentally Neutral Design Outdoor, Inc.',
    'LaCrosse Europe Inc',
    'LaCrosse International, Inc']}]'''
