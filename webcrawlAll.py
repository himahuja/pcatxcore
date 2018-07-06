#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


if __name__ == "__main__":
    search_query = ""
    search_query.replace(" ", "+")
    url = "https://www.google.com/search?q=deep+learnining+nltk+hill+mo+ked"
    # url = "https://chemicalwatch.com/search?q=" + search_query
    driver = webdriver.Chrome('/Users/himanshuahuja/chromedriver')
    # driver = webdriver.Chrome()
    driver.get(url) # opens the URL
    # search_results = driver.find_element_by_xpath("//html/body/div[@id='main']/div[@id='cnt']/div[@class='mw']/div[@id='rcnt']/div[@class='col']/div[@id='center_col']/div[@id='res']/div[@id='search']//div[@id='ires']/div[@id='rso']/div[@class='bkWMgd']/div[@class='srg']/div[@class='g']")#/div[@class='rc']/div[@class='r']")
    search_results = []
    search_results = driver.find_elements_by_css_selector('div.g')
    print(len(search_results))
    for x in range(0,len(search_results)):
        link = search_results[x].find_element_by_tag_name('a')
        link_href = link.get_attribute('href')
        print(link_href)
        # print(search_results[x].tag_name)
        # if search_results[x].is_displayed():


            # search_results[x].click()
    # print(search_results.tag_name)
    # print(search_results.get_attribute('a'))
    # driver.quit()



# GOING TO ADD THE httrack script here for the terminal.
