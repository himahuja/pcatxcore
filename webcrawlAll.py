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
import json, os, re, sys

# ██    ██ ██████  ██          ███    ███  █████  ██   ██ ███████ ██████
# ██    ██ ██   ██ ██          ████  ████ ██   ██ ██  ██  ██      ██   ██
# ██    ██ ██████  ██          ██ ████ ██ ███████ █████   █████   ██████
# ██    ██ ██   ██ ██          ██  ██  ██ ██   ██ ██  ██  ██      ██   ██
#  ██████  ██   ██ ███████     ██      ██ ██   ██ ██   ██ ███████ ██   ██

def urlmaker_sec(queryDic):
    searchText = queryDic['searchText'] if 'searchText' in queryDic else '*'
    formType = queryDic['formType'] if 'formType' in queryDic else '1'
    sic = queryDic['sic'] if 'sic' in queryDic else '*'
    cik = queryDic['cik'] if 'cik' in queryDic else '*'
    startDate = queryDic['startDate'] if 'startDate' in queryDic else '*'
    endDate = queryDic['endDate'] if 'endDate' in queryDic else '*'
    sortOrder = queryDic['sortOrder'] if 'sortOrder' in queryDic else 'Date'
    url = "https://searchwww.sec.gov/EDGARFSClient/jsp/EDGAR_MainAccess.jsp?search_text={}&sort={}&formType=Form{}&isAdv=true&stemming=true&numResults=100&fromDate={}&toDate={}&queryCik={}&querySic={}&numResults=100".format(searchText, sortOrder, formType, startDate, endDate, cik, sic)
    return url


# ██      ██ ███    ██ ██   ██     ███████ ██ ██   ████████ ███████ ██████
# ██      ██ ████   ██ ██  ██      ██      ██ ██      ██    ██      ██   ██
# ██      ██ ██ ██  ██ █████       █████   ██ ██      ██    █████   ██████
# ██      ██ ██  ██ ██ ██  ██      ██      ██ ██      ██    ██      ██   ██
# ███████ ██ ██   ████ ██   ██     ██      ██ ███████ ██    ███████ ██   ██


def linkFilter_google(url):
    filterList = ['youtube', 'facebook', 'twitter', 'vk', 'instagram', 'wired', 'rollingstone', 'linkedin']
    urlList = url.split('.')
    if any(x in urlList for x in filterList):
        return 0
    else:
        return 1


#  ██████   ██████  ██          ███████ ███████  █████  ██████   ██████ ██   ██
# ██       ██       ██          ██      ██      ██   ██ ██   ██ ██      ██   ██
# ██   ███ ██   ███ ██          ███████ █████   ███████ ██████  ██      ███████
# ██    ██ ██    ██ ██               ██ ██      ██   ██ ██   ██ ██      ██   ██
#  ██████   ██████  ███████     ███████ ███████ ██   ██ ██   ██  ██████ ██   ██


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
            if linkFilter_google(link.get_attribute('href')):
                link_href.append(link.get_attribute('href'))
        # Goes to the next page
        try:
            next_page = driver.find_element_by_css_selector('a#pnnext.pn')
            next_page.click()
        except:
            print("There are no more pages to parse.")
            break
    return link_href

# ███████ ███████  █████  ██████   ██████ ██   ██      ██  ██████  ██   ██
# ██      ██      ██   ██ ██   ██ ██      ██   ██     ███ ██  ████ ██  ██
# ███████ █████   ███████ ██████  ██      ███████      ██ ██ ██ ██ █████
#      ██ ██      ██   ██ ██   ██ ██      ██   ██      ██ ████  ██ ██  ██
# ███████ ███████ ██   ██ ██   ██  ██████ ██   ██      ██  ██████  ██   ██

def search_sec10k(url, driver):
    """
        Add the functionality to return the time
    """
    driver.get(url)
    link_href = []
    link_timestamps = []
    while True:
        search_results = []
        search_results = driver.find_elements_by_css_selector('a#viewFiling.filing')
            # timestamps = driver.find_elements_by_css_selector('i.blue')
        if (len(search_results)) <= 1:
            print('No Results were found for the query on this page')
        else:
            for x in range(0, len(search_results)):
                temp_list = search_results[x].get_attribute('text').split()
                # print(temp_list[0])
                """
                    According to the EDGAR portal, <Anything> of 10-K,
                    the keyword 'of' is the second word. We remove these files.

                    Option 2: 10-K is the first word in the title
                """
                if temp_list[0] == '10-K': #option 2
                    # link_timestamps.append(timestamps[x].get_attribute('text'))
                    # print(timestamps[x].get_attribute('text'))
                    # print(search_results[x].get_attribute('href'))
                    link_href.append(search_results[x].get_attribute('href').split('\'')[1])
                    # print(search_results[x].get_attribute('href').split('\'')[1])
        # Go to the next page
        pages = driver.find_elements_by_xpath("//*[@id='header']/tbody/tr[2]/td/a[text() = 'Next']")
        try:
            pages[0].click()
        except:
            print("There are no more pages to parse.")
            break
    return link_href

# ███████ ███████ ████████     ██████  ██████  ██ ██    ██ ███████ ██████
# ██      ██         ██        ██   ██ ██   ██ ██ ██    ██ ██      ██   ██
# ███████ █████      ██        ██   ██ ██████  ██ ██    ██ █████   ██████
#      ██ ██         ██        ██   ██ ██   ██ ██  ██  ██  ██      ██   ██
# ███████ ███████    ██        ██████  ██   ██ ██   ████   ███████ ██   ██

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

def crawlerWrapper(search_query, engine):
    """
        Takes in the query to search for on a portal
        Currently supported portals:
            1. google: searches the google page for that company
            2. sec10k: searches the 10k filing for that company
            3. sec10kall: finds the 10Ks of all the companies
            #TODO: add the dates for finding the 10Ks for all the companies

        INPUT:
            search_query: ANY dictionary with 'name' as a fundamental component,
                          check the specific engine for more details
            #TODO: engine: STRING, default: 'google', engine to be used for performing the query
        OUTPUT:
            Returns nothing
            Saves a pickle file with the name: search_query
    """
    driver = setDriver()

    #  ██████   ██████   ██████   ██████  ██      ███████
    # ██       ██    ██ ██    ██ ██       ██      ██
    # ██   ███ ██    ██ ██    ██ ██   ███ ██      █████
    # ██    ██ ██    ██ ██    ██ ██    ██ ██      ██
    #  ██████   ██████   ██████   ██████  ███████ ███████

    if engine == 'google':
        search_query['name'].replace(" ", "+")
        url = "https://www.google.com/search?q=" + search_query['name']
        # change the number in the line below to limit the number of pages it parses
        links = search_google(url, driver, 2)
        with open('data/parsedLinks/{}.pk'.format(re.sub('[^A-Za-z]+', '', search_query['name'])), 'wb') as handle:
            pk.dump(links, handle, protocol=pk.HIGHEST_PROTOCOL)

    # ███████ ███████  ██████    ██  ██████  ██   ██
    # ██      ██      ██        ███ ██  ████ ██  ██
    # ███████ █████   ██         ██ ██ ██ ██ █████
    #      ██ ██      ██         ██ ████  ██ ██  ██
    # ███████ ███████  ██████    ██  ██████  ██   ██

    elif engine == 'sec10k':
        """
        search query format:
        TYPE: dictionary
        {cik: <STRING, CIK Code of the company>,
         dateStart: <STRING, '/' seperated date, MM/DD/YYYY>,
         dateEnd: <STRING, '/' seperated date, MM/DD/YYYY>,}
        """
        search_query['formType'] = "10K"
        url = urlmaker_sec(search_query)
        links = search_sec10k(url, driver)
        with open('data/parsedLinks/{}.pk'.format(search_query['cik']), 'wb') as handle:
            pk.dump(links, handle, protocol=pk.HIGHEST_PROTOCOL)
        # print(timestamps)

    #  █████  ██      ██           ██  ██████  ██   ██
    # ██   ██ ██      ██          ███ ██  ████ ██  ██
    # ███████ ██      ██           ██ ██ ██ ██ █████
    # ██   ██ ██      ██           ██ ████  ██ ██  ██
    # ██   ██ ███████ ███████      ██  ██████  ██   ██

    elif engine == 'sec10kall':
        """
            uses the sec10k engine and list of cik keywords to get the 10Ks of all the companies in the SEC list
        """
        search_query['formType'] = "10K"
        try:
            with open('data/SEC_data/cikcodes2name.pk', 'rb') as f:
                cikcodes2name = pk.load(f)
        except:
            print('Couldn\'t locate the file: cikcodes2name.pk')
            return

        for cik in cikcodes2name.keys():
            search_query['cik'] = cik
            url = urlmaker_sec(search_query)
            print(url)
            links = search_sec10k(url, driver)
            with open('data/parsedLinks/ALL_{}.pk'.format(search_query['cik']), 'wb') as handle:
                pk.dump(links, handle, protocol=pk.HIGHEST_PROTOCOL)

    # ███████ ███████  ██████     ███████ ██  ██████
    # ██      ██      ██          ██      ██ ██
    # ███████ █████   ██          ███████ ██ ██
    #      ██ ██      ██               ██ ██ ██
    # ███████ ███████  ██████     ███████ ██  ██████

    elif engine == 'secsic10k':
        """
            uses the SIC codes to gather all the companies' 10K in that particular SIC
            DICT elements, dateStart, dateEnd
        """
        search_query['formType'] = "10K"
        try:
            with open('data/SEC_data/siccodes2name.pk', 'rb') as f:
                siccodes2name = pk.load(f)
        except:
            print('Couldn\'t locate the file: siccodes2name.pk')
            return

        for sic in siccodes2name.keys():
            search_query['sic'] = sic
            url = urlmaker_sec(search_query)
            links = search_sec10k(url, driver)
            with open('data/parsedLinks/SIC_{}.pk'.format(search_query['sic']), 'wb') as handle:
                pk.dump(links, handle, protocol=pk.HIGHEST_PROTOCOL)

    # ███████ ███████  ██████      ██████  ███████ ███    ██ ███████ ██████   █████  ██
    # ██      ██      ██          ██       ██      ████   ██ ██      ██   ██ ██   ██ ██
    # ███████ █████   ██          ██   ███ █████   ██ ██  ██ █████   ██████  ███████ ██
    #      ██ ██      ██          ██    ██ ██      ██  ██ ██ ██      ██   ██ ██   ██ ██
    # ███████ ███████  ██████      ██████  ███████ ██   ████ ███████ ██   ██ ██   ██ ███████

    elif engine == "generalSEC":
        url = urlmaker_sec(search_query)
        driver.get(url)
        # links = search_sec(url, driver)

    # ███████ ███████  ██████     ███████     ██████   ██
    # ██      ██      ██          ██               ██ ███
    # ███████ █████   ██          █████        █████   ██
    #      ██ ██      ██          ██          ██       ██
    # ███████ ███████  ██████     ███████     ███████  ██

    elif engine == 'secE21':
        """
            uses the company CIK to find if it has any subidaries from the E-21 form
        """

    elif engine == 'bloomberg':
        pass
    elif engine == 'sitespecific':
        pass

    else:
        print("Engine hasn't been defined yet.")
    # search_results = driver.find_element_by_xpath("//html/body/div[@id='main']/div[@id='cnt']/div[@class='mw']/div[@id='rcnt']/div[@class='col']/div[@id='center_col']/div[@id='res']/div[@id='search']//div[@id='ires']/div[@id='rso']/div[@class='bkWMgd']/div[@class='srg']/div[@class='g']")#/div[@class='rc']/div[@class='r']")
    driver.quit()

if __name__ == "__main__":
    search_query = {}
    """ Using the google crawler"""
    # search_query['name'] = "whatever you want to query on google"
    # crawlerWrapper('Hello I am Himanshu Ahuja what is python we love code wtf', 'google')
    """ Using the SEC CIK 10k engine on one of the CIKs"""
    # search_query['name'] = '1000045_CIK'
    # search_query['cik'] = '1000045'
    # search_query['dateStart'] = '08/05/2016'
    # search_query['dateEnd'] = '08/05/2019'
    # crawlerWrapper(search_query, 'sec10k')

    """ Using the SEC CIK 10k engine on all of the CIK"""
    search_query['name'] = "All"
    search_query['dateStart'] = '08/05/2015'
    search_query['dateEnd'] = '08/05/2019'
    crawlerWrapper(search_query, 'sec10kall')

    """ Using the SEC for an SIC"""
    # search_query['dateStart'] = '08/05/2015'
    # search_query['dateEnd'] = '08/05/2019'
    # crawlerWrapper(search_query, 'secsic10k')
