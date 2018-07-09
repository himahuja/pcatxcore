#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# to set the browser options
from selenium.webdriver.chrome.options import Options
# to set the wait time before moving to the next page
from selenium.webdriver.support import expected_conditions as EC
# to save python objects
import pickle as pk
import json
import os

def linkFilter_google(url):
    filterList = ['youtube', 'facebook', 'twitter', 'vk', 'instagram', 'wired', 'rollingstone']
    urlList = url.split('.')
    if any(x in urlList for x in filterList):
        return 0
    else:
        return 1

def linkFilter_SEC(url):

def search_google(query, driver, number_of_pages):
    driver.get(query)
    link_href = []
    for i in range(number_of_pages):
        search_results = []
        # finds all the search boxes in a page
        search_results = driver.find_elements_by_css_selector('h3.r')
        for x in range(0,len(search_results)):
        # TODO: Associate each link with the rank it appeared on google
            link = search_results[x].find_element_by_tag_name('a')
            if linkFilter(link.get_attribute('href')):
                link_href.append(link.get_attribute('href'))
        # Goes to the next page
        try:
            next_page = driver.find_element_by_css_selector('a#pnnext.pn')
            next_page.click()
        except:
            print("There are no more pages to parse.")
            break
    return link_href

def search_sec(query, driver):
    driver.get(query)
    link_href = []
    while True:
        search_results = []
        search_results = driver.find_elements_by_css_selector('a#viewFiling.filing')
        for x in range(0, len(search_results)):
            temp_list = search_results[x].get_attribute('text').split()
            """
                According to the EDGAR portal, <Anything> of 10-K,
                the keyword 'of' is the second word. We remove these files.

                Option 2: 10-K is the first word in the title
            """
            if temp_list[0] == '10-K':
                link_href.append(search_results[x].get_attribute('href').split('\'')[2])
    return link_href

def setDriver():
    path_chromedriver = os.path.join(os.path.dirname(os.path.realpath(__file__)), "chromedriver")
    options = Options()
    options.add_argument("--headless") # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox') # Bypass OS security model
    options.add_argument('--disable-gpu')  # applicable to windows os only
    options.add_argument('start-maximized') #
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(path_chromedriver, chrome_options=options)
    return driver

def crawlerWrapper(search_query, engine):
    """
        Takes in the query to search for on a portal
        Currently supported portals:
            1. google: searches the google page for that company
            2. sec10k: searches the 10k filing for that company
            3. sec10kall: finds the 10Ks of all the companies
            #TODO: add the dates for finding the 10Ks for all the companies

        INPUT:
            search_query: ANY, check the specific engine for more details
            #TODO: engine: STRING, default: 'google', engine to be used for performing the query
        OUTPUT:
            Returns nothing
            Saves a pickle file with the name: search_query
    """
    driver = setDriver()

    if engine == 'google':
        search_query.replace(" ", "+")
        url = "https://www.google.com/search?q=" + search_query
        # change the number in the line below to limit the number of pages it parses
        links = search_google(url, driver, 2)
    elif engine == 'sec10k':
        """
        search query format:
        TYPE: dictionary
        {name: <STRING, CIK Code of the company>,
         dateStart: <STRING, '/' seperated date, MM/DD/YYYY>,
         dateEnd: <STRING, '/' seperated date, MM/DD/YYYY>,}
        """
        #TODO: Module on hold, because of the errorneous results
        cik = search_query['cik']
        # name = search_query['name']
        dateStart = search_query['dateStart']
        dateEnd = search_query['dateEnd']
        # name.replace(" ", "%20")
        url = "https://searchwww.sec.gov/EDGARFSClient/jsp/EDGAR_MainAccess.jsp?search_text=*&sort=Date&formType=Form10K&isAdv=true&stemming=true&numResults=100&queryCik={}&fromDate={}&toDate={}&numResults=100".format(cik, dateStart, dateEnd)
        # url = "https://searchwww.sec.gov/EDGARFSClient/jsp/EDGAR_MainAccess.jsp?search_text={}&sort=Date&formType=Form10K&isAdv=true&stemming=true&numResults=100&fromDate={}&toDate={}}&numResults=100".
        search_sec(url, driver)
    elif engine == 'sec10kall'

    elif engine == 'bloomberg':
        pass
    else:
        print("Engine hasn't been defined yet.")

    with open('data/parsedLinks/{}.pk'.format(search_query), 'wb') as handle:
        pk.dump(links, handle, protocol=pk.HIGHEST_PROTOCOL)
    # search_results = driver.find_element_by_xpath("//html/body/div[@id='main']/div[@id='cnt']/div[@class='mw']/div[@id='rcnt']/div[@class='col']/div[@id='center_col']/div[@id='res']/div[@id='search']//div[@id='ires']/div[@id='rso']/div[@class='bkWMgd']/div[@class='srg']/div[@class='g']")#/div[@class='rc']/div[@class='r']")
    driver.quit()

if __name__ == "__main__":
    crawlerWrapper('Hello I am Himanshu Ahuja what is python we love code wtf', 'google')
    # search_query = "deep learning"
    # search_query.replace(" ", "+")
    # url = "https://www.google.com/search?q=" + search_query
    # # url = "https://chemicalwatch.com/search?q=" + search_query
    # driver = setDriver()
    # links = search_google(url, driver)
    # with open('filename.pickle', 'wb') as handle:
    #     pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)
    # # driver = webdriver.Chrome()
    # # driver.get(url) # opens the URL
    # # search_results = driver.find_element_by_xpath("//html/body/div[@id='main']/div[@id='cnt']/div[@class='mw']/div[@id='rcnt']/div[@class='col']/div[@id='center_col']/div[@id='res']/div[@id='search']//div[@id='ires']/div[@id='rso']/div[@class='bkWMgd']/div[@class='srg']/div[@class='g']")#/div[@class='rc']/div[@class='r']")
    # driver.quit()
# GOING TO ADD THE httrack script here for the terminal.
