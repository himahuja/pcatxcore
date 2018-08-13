# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 12:22:46 2018

@author: Melody
"""

import time
from selenium import webdriver
import pickle
import json, os, re, sys, subprocess
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

# IMPORTANT NOTE: unlike other crawler drivers, ewg driver needs to be set as NON-HEADLESS which means
# the user can see the process of crawling in the browser
# The user must manually close pop-up ads for the crawler to function
 
def setDriver():
    options = Options()
    #options.add_argument("--headless") # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox') # Bypass OS security model
    options.add_argument('--disable-gpu')  # applicable to windows os only
    options.add_argument('start-maximized') #
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(chrome_options=options)
    return driver

# find all products for a company
def company_to_product(company,driver):
    
    comp_prod_dict = {}
    try:
        url = 'https://www.ewg.org/skindeep/search.php?query=&search_group=companies&ptype2=#.W2nG9P5Kgxe'
        driver.get(url)
        time.sleep(10)
        # find the search bar and enter the company name
        driver.find_element_by_xpath("//input[@name='query' and @value=' query' and @id='imageSearch']").clear()
        driver.find_element_by_xpath("//input[@name='query' and @value=' query' and @id='imageSearch']").send_keys(company)
        driver.find_element_by_xpath("//input[@type='submit' and @onclick='this.form.submit();']").click()
        # find and click on the link to product list
        atags = driver.find_elements_by_tag_name("a")
        for a in atags:
            if 'product' in a.text:
                a.click()
                break   
        # display the search results as 50 items a page
        atags2 = driver.find_elements_by_tag_name("a")
        for a in atags2:
            if a.text == '50':
                a.click()
                break
        # find the tags containing product names and add to product list for the company
        prod_list = []
        while True:   
            try:
                td_list = driver.find_elements_by_xpath("//td[@class='product_name_list']")
                for td in td_list:
                    prod_list.append(td.find_element_by_tag_name('a').text)   
            except:
                break
            try:
                atags3 = driver.find_element_by_xpath("//div[@id='click_next_number' and @class='light']").find_elements_by_tag_name('a')
            except:
                break
            # keep going if there's next page
            try:
                found = False
                for a in atags3:
                    if a.text == 'Next>':
                        found = True
                        a.click()
                        time.sleep(2)
                if not found:
                    print(company+' products attached.')
                    break
            except:
                break
        # map a company to a product list once found
        if prod_list != []:
            comp_prod_dict[company] = prod_list
        time.sleep(4)
        
    except:
        print(company+' not found')
        time.sleep(4)
    return comp_prod_dict

# find ingredients for all products
def product_to_ingredient(comp_prod_dict,driver):
    comp_prod_ingredient_dict = {}
    for key in comp_prod_dict:
        prod_ingredient_dict = {}
        for prod in comp_prod_dict[key]:
            try:
                url = 'https://www.ewg.org/skindeep/search.php?query=&search_group=products&ptype2=#.W2sehdJKiUl'
                driver.get(url)
                driver.find_element_by_xpath("//input[@name='query' and @value=' query' and @id='imageSearch']").clear()
                driver.find_element_by_xpath("//input[@name='query' and @value=' query' and @id='imageSearch']").send_keys(prod)
                driver.find_element_by_xpath("//input[@type='submit' and @onclick='this.form.submit();']").click()
                atags = driver.find_element_by_xpath("//table[@id='table-browse' and @sean_marker='a4']").find_elements_by_tag_name('a')
                # find and click on the product returned by search results
                for a in atags:
                    if a.text == prod:
                        a.click()
                        break
                # find the tags containing ingredients information and get the contents
                td_list = driver.find_elements_by_xpath("//td[@class='firstcol']")
                ingredient_list = []
                
                for td in td_list:
                    if td.text != '':
                        ingredient_list.append(td.text.replace('\n',' '))
                if ingredient_list != []:
                    prod_ingredient_dict[prod] = ingredient_list
                    print(prod+' ingredient found')
                time.sleep(4)
    
            except:
                print(prod+' ingredient not found')
                time.sleep(4)
        if prod_ingredient_dict != {}:
            comp_prod_ingredient_dict[key] = prod_ingredient_dict
    return comp_prod_ingredient_dict

if __name__ == "__main__":
    driver = setDriver()
    # example ewg company name: Advanced Research Laboratories, Advanced Beauty, Inc.
    company = input('Please enter a company name: ')
    comp_prod_dict = company_to_product(company,driver)
    print(product_to_ingredient(comp_prod_dict,driver))