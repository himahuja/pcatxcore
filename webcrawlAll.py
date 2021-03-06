#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Himanshu, Melody, Alex
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# to set the browser options
from selenium.webdriver.chrome.options import Options
# to set the wait time before moving to the next page
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
# to save python objects
import pickle as pk
import json, os, re, sys, subprocess, time
from collections import OrderedDict

# ██    ██ ██████  ██          ███    ███  █████  ██   ██ ███████ ██████
# ██    ██ ██   ██ ██          ████  ████ ██   ██ ██  ██  ██      ██   ██
# ██    ██ ██████  ██          ██ ████ ██ ███████ █████   █████   ██████
# ██    ██ ██   ██ ██          ██  ██  ██ ██   ██ ██  ██  ██      ██   ██
#  ██████  ██   ██ ███████     ██      ██ ██   ██ ██   ██ ███████ ██   ██

def urlmaker_sec(queryDic):
    """
    Produces the URL, which can be entered into the search (Designed for SEC.gov)


    Parameters
    ----------
    queryDic : dict
        searchText (str): Company name to be searched (Default: '*')
        formType (str): Type of the document to be retrieved (Default: '1')
        sic (str): SIC code for the companies to be searched (Default: '*')
        cik (str): CIK code for the company to be searched (Default: '*')
        startDate (str): Start date of the produced results (YYYYMMDD) (Default: '*')
        endDate (str): End date of the produced results (YYYYMMDD) (Default: '*')
        sortOrder (str): Ascending (Value = 'Date') or Descending (Value = 'ReverseDate') retrieval of results, (Default: 'Date')

    Returns
    -------
    str
        URL to be searched on the SEC website
    """
    #query for SEC
    searchText = queryDic['searchText'] if 'searchText' in queryDic else '*'
    formType = queryDic['formType'] if 'formType' in queryDic else '1'
    sic = queryDic['sic'] if 'sic' in queryDic else '*'
    cik = queryDic['cik'].lstrip('0') if 'cik' in queryDic else '*'
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
    """
    Filters out the links of social media websites from the returned google search results using `filterList` defined implicitly.


   Parameters
    ----------
    url : str
        URL to be tested against `filterList`

    Returns
    -------
    int
        returns 0 (is a social media link), 1 (is not a social media link)
    """
    filterList = ['youtube', 'facebook', 'twitter', 'vk', 'instagram', 'wired', 'rollingstone', 'linkedin']
    filterList.extend(['https://'+ k for k in filterList])
    filterList.extend(['http://'+ k for k in filterList])
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
    """
        Searches Google websites for the top page results


        Parameters
        ----------
        query : dict
            name (str): the mandatory portion of the search query
            aliases (str[]): optional words of the search query
            filetype (str): filetype to be searched for
        driver : selenium.webdriver.Chrome
            An instance of browser driving engine
        number_of_pages : int
            Number of pages of Google web results

        Returns
        -------
        list of strings
            list of links returned from the Google search engine
    """
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
            #hopefully helps us from getting blocked
            time.sleep(.5)
            next_page.click()
        except Exception as e:
            print("There are no more pages to parse. {}".format(str(e)))
            break
    return link_href

# ███████ ███████  █████  ██████   ██████ ██   ██      ██  ██████  ██   ██
# ██      ██      ██   ██ ██   ██ ██      ██   ██     ███ ██  ████ ██  ██
# ███████ █████   ███████ ██████  ██      ███████      ██ ██ ██ ██ █████
#      ██ ██      ██   ██ ██   ██ ██      ██   ██      ██ ████  ██ ██  ██
# ███████ ███████ ██   ██ ██   ██  ██████ ██   ██      ██  ██████  ██   ██

def search_sec10k(url, driver):
    """
        @Deprecated module
    """
    driver.get(url)
    link_href = []
    link_timestamps = []
    while True:
        search_results = []
        search_results = driver.find_elements_by_css_selector('a#viewFiling.filing')
            # timestamps = driver.find_elements_by_css_selector('i.blue')
        if (len(search_results)) <= 1:
            print('No Results were found for the query: {}'.format(search_query['cik']))
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
        except NoSuchElementException:
            raise Exception("We are unable to reach Google")
    return link_href

# ███████ ███████ ████████     ██████  ██████  ██ ██    ██ ███████ ██████
# ██      ██         ██        ██   ██ ██   ██ ██ ██    ██ ██      ██   ██
# ███████ █████      ██        ██   ██ ██████  ██ ██    ██ █████   ██████
#      ██ ██         ██        ██   ██ ██   ██ ██  ██  ██  ██      ██   ██
# ███████ ███████    ██        ██████  ██   ██ ██   ████   ███████ ██   ██

def setDriver(headless = False):
    """
        Sets a selenium webdriver object for running web-crawlers on various systems.
        Note: Requires chromedrivers for various platforms in a chromedrivers directory

        Parameters
        ----------
        headless : Boolean
            if True, sets a headless browser. if False (Default), sets a browser with head

        Returns
        -------
        selenium.webdriver.Chrome
            driver with standard option settings
    """
    if sys.platform == 'darwin':
        type_chromedriver = "chromedriver_darwin"
    elif sys.platform == 'linux':
        type_chromedriver = "chromedriver_linux"
    elif sys.platform == 'win32':
        type_chromedriver = "chromedriver_win32.exe"
    path_chromedriver = os.path.join(os.path.dirname(os.path.realpath(__file__)), "chromedrivers", type_chromedriver)
    options = Options()
    if headless:
        options.add_argument("--headless") # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox') # Bypass OS security model
    options.add_argument('--disable-gpu')  # applicable to windows os only
    options.add_argument('start-maximized') #
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(path_chromedriver, chrome_options=options)
    return driver


    #  ██████ ██████   █████  ██     ██ ██      ███████ ██████      ██     ██ ██████   █████  ██████
    # ██      ██   ██ ██   ██ ██     ██ ██      ██      ██   ██     ██     ██ ██   ██ ██   ██ ██   ██
    # ██      ██████  ███████ ██  █  ██ ██      █████   ██████      ██  █  ██ ██████  ███████ ██████
    # ██      ██   ██ ██   ██ ██ ███ ██ ██      ██      ██   ██     ██ ███ ██ ██   ██ ██   ██ ██
    #  ██████ ██   ██ ██   ██  ███ ███  ███████ ███████ ██   ██      ███ ███  ██   ██ ██   ██ ██

def crawlerWrapper(search_query, engine, doSetDriver, headless = False):
    """
        Takes in the query to search for on a portal.
        NOTE: Saves to file, does not return anything.

        Currently supported portals:
            1. google: searches the google page for entered company
            2. sec10k: searches the 10k filing for that company
            3. sec10kall: finds the 10Ks of all the companies
            4. secsic10k: uses the SIC codes to gather all the companies' 10K in all SICs
            5. generalSEC: performs any general query on SEC using `urlmaker_sec`
            6. sitespecific: Performs Crawling specifically on any particular website
            7. tri: Returns the TRI page for given facility ID
            8. everything-all: finds the 8Ks, 10Ks and EX-21s of all the companies on the SEC website, via CIK


        Parameters
        ----------
            search_query : dict
                The format for search query for different engines is as follows:
                1. google
                    name (str): the mandatory portion of the search query
                    aliases (str[]): optional words of the search query
                    filetype (str): filetype to be searched for
                2. sec10k:
                    cik (str): String typed CIK code of the company
                    dateStart (str): Starting date of filings, '/' seperated date, MM/DD/YYYY
                    dateEnd (str): Ending date of filings, '/' seperated date, MM/DD/YYYY
                3. sec10kall:
                    None
                4. secsic10k:
                    None
                5. generalSEC:
                    searchText (str): Company name to be searched (Default: '*')
                    formType (str): Type of the document to be retrieved (Default: '1')
                    sic (str): SIC code for the companies to be searched (Default: '*')
                    cik (str): CIK code for the company to be searched (Default: '*')
                    startDate (str): Start date of the produced results (YYYYMMDD) (Default: '*')
                    endDate (str): End date of the produced results (YYYYMMDD) (Default: '*')
                    sortOrder (str): Ascending (Value = 'Date') or Descending (Value = 'ReverseDate') retrieval of results, (Default: 'Date')
                6. tri:
                    tri_id (str): TRI ID of the facility
                7. google-subs:
                    name: name of the company whose subsidiaries have to be discovered
                8. everything-all:
                    None
            search_query: str
                1. sitespecific:
                    Default Settings:
                        1. -p0: only parse URLS, don't download anything
                        2. -%I : make an index of links
                        3. set depth of 5
                        4. language preference: en
                        5. -n: get non-html files near an html

                    search_query['name']: url of the website we need to download
                    -O output directory
                    -r<number> set the depth limit
                    -m<number>,<number> nonhtml,html file size limit in bytes
                    %e<number>, number of external links from the targetted website
                    '%P0' don't attempt to parse link in Javascript or in unknown tags
                    -n get non-html files near an HTML-files (images on web-pages)
                    t test all urls
                    -%L <filename>, loads all the links to be tracked by the function
                    K0 Keep relative links
                    K keep original links
                    -%l "en, fr, *" language preferences for the documents
                    -Z debug log
                    -v verbose screen mode
                    I make an index
                    %I make a searchable index
                    -pN priority mode (0): just scan (1): just get html (2): just get non-html (3): save all files (7): get html files first, then treat other files
            engine: str
                specify which type of crawler to use, refer module summary for options

        Returns
        -------
            None

    """
    if doSetDriver == None:
        driver = setDriver(headless)
    else:
        driver = doSetDriver

    #  ██████   ██████   ██████   ██████  ██      ███████
    # ██       ██    ██ ██    ██ ██       ██      ██
    # ██   ███ ██    ██ ██    ██ ██   ███ ██      █████
    # ██    ██ ██    ██ ██    ██ ██    ██ ██      ██
    #  ██████   ██████   ██████   ██████  ███████ ███████

    if engine == 'google':
        search_query['name'].replace(" ", "+")
        search_query['name'] = '"' + search_query['name'] + '"'
        url = "https://www.google.com/search?q=" + search_query['name']
        try:
            search_query['aliases'] = ["+~" + s for s in search_query['aliases']]
            for optional in search_query['aliases']:
                url += optional
        except:
            pass
            # print("There are no aliases")
        try:
            search_query['filetype'] = "+filetype:%3A" + search_query['filetype']
            url += search_query['filetype']
        except:
            pass
            # print("There is no file type specified")
        # change the number in the line below to limit the number of pages it parses
        links = search_google(url, driver, 2)
        with open('data/parsedLinks/{}.pk'.format(re.sub('[^0-9A-Za-z-]+', '', search_query['name'])), 'wb') as handle:
            pk.dump(links, handle, protocol=pk.HIGHEST_PROTOCOL)

    # ███████ ███████  ██████    ██  ██████  ██   ██
    # ██      ██      ██        ███ ██  ████ ██  ██
    # ███████ █████   ██         ██ ██ ██ ██ █████
    #      ██ ██      ██         ██ ████  ██ ██  ██
    # ███████ ███████  ██████    ██  ██████  ██   ██

    elif engine == 'sec10k':
        search_query['formType'] = "10K"
        url = urlmaker_sec(search_query)
        links = search_sec10k(url, driver)
        with open('data/parsedLinks/{}.pk'.format(search_query['cik']), 'wb') as handle:
            pk.dump(links, handle, protocol=pk.HIGHEST_PROTOCOL)
        print(links)

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
            print('Couldn\'t locate the file: cik10k.pk')
            return
        try:
            with open('data/SEC_data/cik10Kall.pk', 'rb') as f:
                cik10k = pk.load(f)
                print('Loaded Old file!')
        except:
            cik10k = {}
        count = 0
        cikcodes2name = OrderedDict(sorted(cikcodes2name.items(), key=lambda t: t[0]))

        for cik in list(cikcodes2name.keys())[len(cik10k)+1:]:
            count = count + 1
            search_query['cik'] = cik
            url = urlmaker_sec(search_query)
            # print(url)
            links = search_sec10k(url, driver)
            cik10k[search_query['cik']] = links
            if count%1000 == 0:
                print('Saing the first {} CIKs'.format(count))
                with open('data/SEC_data/cik10Kall.pk', 'wb') as handle:
                    pk.dump(cik10k, handle, protocol=pk.HIGHEST_PROTOCOL)

    # ███████ ███████  ██████     ███████ ██  ██████
    # ██      ██      ██          ██      ██ ██
    # ███████ █████   ██          ███████ ██ ██
    #      ██ ██      ██               ██ ██ ██
    # ███████ ███████  ██████     ███████ ██  ██████

    elif engine == 'secsic10k':
        """
            uses the SIC codes to gather all the companies' 10K in that particular SIC
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
        links = []
        # links = search_sec(url, driver)

    # ███████ ██ ████████ ███████     ███████ ███████  █████  ██████   ██████ ██   ██
    # ██      ██    ██    ██          ██      ██      ██   ██ ██   ██ ██      ██   ██
    # ███████ ██    ██    █████       ███████ █████   ███████ ██████  ██      ███████
    #      ██ ██    ██    ██               ██ ██      ██   ██ ██   ██ ██      ██   ██
    # ███████ ██    ██    ███████     ███████ ███████ ██   ██ ██   ██  ██████ ██   ██

    elif engine == 'sitespecific':
        url = search_query['url']
        name = search_query['name']
        filename = 'sitespecific.sh'
        path_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", filename)
        """
            Current settings:

        """
        caller_statement = "httrack {} -O data/temp/{} -r5 -n '%P0' -%I -p0 -%l \"en\" '-* +*htm +*html +*pdf'".format(url, name)
        with open(path_file, 'w') as handle:
            # makes sure that it runs a bash script
            handle.write('#!/bin/sh' + '\n')
            # adds the line for the
            handle.write(caller_statement)
        # os.chmod(path_file, stat.S_IREAD | stat.S_IRGRP | stat.S_IROTH | stat.S_IXOTH | stat.S_IXUSR | stat.S_IXGRP)
        subprocess.call(['chmod', '777', 'data/{}'.format(filename)])
        subprocess.call(['./data/{}'.format(filename)])
        links = []

    # ████████ ██████  ██
    #    ██    ██   ██ ██
    #    ██    ██████  ██
    #    ██    ██   ██ ██
    #    ██    ██   ██ ██

    elif engine == 'tri':
        tri_id = search_query['tri_id']
        url = 'https://www3.epa.gov/enviro/facts/tri/ef-facilities/#/Facility/'+tri_id
        return url


    #  ██████   ██████   ██████  ██          ███████ ██    ██ ██████  ███████
    # ██       ██    ██ ██       ██          ██      ██    ██ ██   ██ ██
    # ██   ███ ██    ██ ██   ███ ██          ███████ ██    ██ ██████  ███████
    # ██    ██ ██    ██ ██    ██ ██               ██ ██    ██ ██   ██      ██
    #  ██████   ██████   ██████  ███████     ███████  ██████  ██████  ███████

    elif engine == 'google-subs':
        search_query['name'].replace(" ", "+")
        url = "https://www.google.com/search?q=" + search_query['name'] + '+subsidiaries'
        return url


    #  █████  ██   ██      ██  ██████  ██   ██     ███████ ██████   ██
    # ██   ██ ██  ██      ███ ██  ████ ██  ██      ██           ██ ███
    #  █████  █████        ██ ██ ██ ██ █████       █████    █████   ██
    # ██   ██ ██  ██       ██ ████  ██ ██  ██      ██      ██       ██
    #  █████  ██   ██      ██  ██████  ██   ██     ███████ ███████  ██

    elif engine == 'everything-all':
        try:
            with open('data/SEC_Data/cikcodes2name.pk', 'rb') as f:
                cikcodes2name = pk.load(f)
        except:
            print('Couldn\'t locate the file: cikcodes2name.pk')
            return
        try:
            with open('data/SEC_Data/bigedgar_part{}.pk'.format(search_query['part']), 'rb') as f:
                bigedgar = pk.load(f)
                print('Loaded Old file!')
        except:
            bigedgar = {}
        count = 0
        cikcodes2name = OrderedDict(sorted(cikcodes2name.items(), key=lambda t: t[0]))
        starting_length = len(bigedgar)
        for cik in list(cikcodes2name.keys())[search_query['starting_point']+starting_length:search_query['ending_point']]:
            count = count + 1
            k8_info = []
            k10_info = []
            ex21_info = []
            ## GET the 8-Ks
            try:
                start = 0
                while True:
                    url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type=8-K&dateb=&owner=include&start={}&count=100'.format(cik, start)
                    driver.get(url)
                    # if start == 0:
                    #     mails = driver.find_elements_by_css_selector('span.mailerAddress')
                    #     for mail in mails:
                    #         bigedgar[cik]['edgar_mailing_address'] += mail.get_attribute('text')
                    rows = driver.find_elements_by_xpath('//*[@id="seriesDiv"]/table/tbody/tr[position() >= 2 and position() <= last()]')
                    for row in rows:
                        col = row.find_elements_by_tag_name("td")
                        if col[0].text == '8-K':
                            ## The if condition skips the amendment in 8-K
                            per_k8_info = {}
                            per_k8_info['time_of_filing'] = col[3].text
                            # print(col[1].text)
                            documentButtons = col[1].find_elements_by_tag_name('a')
                            for documentButton in documentButtons:
                                if documentButton.get_attribute('id') == 'documentsbutton':
                                    per_k8_info['url'] = documentButton.get_attribute('href')
                                    break
                            # print(per_k8_info)
                            k8_info.append(per_k8_info)

                    buttons = driver.find_elements_by_xpath('//*[@id="contentDiv"]/div[3]/form/table/tbody/tr/td[2]/input')

                    flag = 0

                    for button in buttons:
                        if button.get_attribute('value') == 'Next 100':
                            start = start + 100
                            flag = 1
                            break
                    if flag == 0:
                        # print("There are no more 8-K pages for CIK: {}+len(bigedgar)".format(cik))
                        break

                for per_k8_info in k8_info:
                    driver.get(per_k8_info['url'])
                    # //*[@id="formDiv"]/div/table/tbody/tr[2]/td[1]
                    # rows_in = driver.find_elements_by_xpath('//*[@id="formDiv"]/div/table/tbody/tr[position() >=2 and position <= last()]')
                    # print(rows_in)
                    rows_in = driver.find_elements_by_css_selector('tr')
                    for row_in in rows_in:
                        try:
                            col_in = row_in.find_elements_by_tag_name("td")
                            if len(col_in) != 0:
                        # print(col_in[3])
                                if col_in[3].text == '8-K':
                                # print(col_in[2])
                                    if col_in[2].text != '':
                                        per_k8_info['url'] = col_in[2].find_element_by_tag_name('a').get_attribute('href')
                                    else:
                                        per_k8_info['url'] = ""
                                # print(col_in[2].find_element_by_tag_name('a').get_attribute('href'))
                                # print(per_k8_info['url'])
                                break
                        except:
                            print("Problems inside the 8-k parser, CIK: {}".format(cik))
                            pass

                # Get the 10K and the E-21s
                start = 0
                while True:
                    url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type=10-K&dateb=&owner=include&start={}&count=100'.format(cik, start)
                    driver.get(url)
                    rows = driver.find_elements_by_xpath('//*[@id="seriesDiv"]/table/tbody/tr[position() >= 2 and position() <= last()]')
                    for row in rows:
                        col = row.find_elements_by_tag_name("td")
                        if col[0].text == '10-K':
                            # to skip amendments in 10-Ks
                            per_k10_info = {}
                            per_k10_info['time_of_filing'] = col[3].text
                            documentButtons = col[1].find_elements_by_tag_name('a')
                            for documentButton in documentButtons:
                                if documentButton.get_attribute('id') == 'documentsbutton':
                                    per_k10_info['url'] = documentButton.get_attribute('href')
                                    break
                            k10_info.append(per_k10_info)
                    buttons = driver.find_elements_by_xpath('//*[@id="contentDiv"]/div[3]/form/table/tbody/tr/td[2]/input')


                    flag = 0

                    for button in buttons:
                        if button.get_attribute('value') == 'Next 100':
                            start = start + 100
                            flag = 1
                            break
                    if flag == 0:
                        # print("There are no more 10-K pages for CIK: {}".format(cik))
                        break

                for per_k10_info in k10_info:
                    driver.get(per_k10_info['url'])
                    # rows_in = driver.find_elements_by_xpath('//*[@id="formDiv"]/div/table/tbody/tr[position()>=2 and position <= last()]')
                    rows_in = driver.find_elements_by_css_selector('tr')
                    for row_in in rows_in:
                        try:
                            col_in = row_in.find_elements_by_tag_name("td")
                            if len(col_in) != 0:
                                if col_in[3].text == '10-K':
                                    if col_in[2].text != '':
                                        per_k10_info['url'] = col_in[2].find_element_by_tag_name('a').get_attribute('href')
                                    else:
                                        per_k10_info['url'] = ""
                                elif col_in[3].text == 'EX-21':
                                    per_ex21_info = {}
                                    per_ex21_info['time_of_filing'] = per_k10_info['time_of_filing']
                                    if col_in[2].text != '':
                                        per_ex21_info['url'] = col_in[2].find_element_by_tag_name('a').get_attribute('href')
                                    else:
                                        per_ex21_info['url'] = ""
                                    ex21_info.append(per_ex21_info)
                        except:
                            print('10K Problem in pages inside, CIK: {}'.format(cik))
                            pass

                bigedgar[cik] = {'8K': k8_info, '10K': k10_info, 'EX21': ex21_info}
                # Save every 200 files
                if count%100 == 0 or count == (search_query['ending_point']-search_query['starting_point']):
                    print("Completed {}/{} in part {}.".format(count, search_query['ending_point']-search_query['starting_point'], search_query['part']))
                    # print('Saving the first {} items'.format(count))
                    with open('data/SEC_Data/bigedgar_part{}.pk'.format(search_query['part']), 'wb') as handle:
                        pk.dump(bigedgar, handle, protocol=pk.HIGHEST_PROTOCOL)
                    with open('data/SEC_Data/error_cik.pk', 'wb') as handle:
                        pk.dump(error_cik, handle, protocol=pk.HIGHEST_PROTOCOL)
            except:
                try:
                    with open('data/SEC_Data/error_cik.pk', 'rb') as f:
                        error_cik = pk.load(f)
                except:
                    error_cik = []
                print('Error in CIK: {}'.format(cik))
                error_cik.append(cik)
                with open('data/SEC_Data/error_cik.pk', 'wb') as handle:
                    pk.dump(error_cik, handle, protocol=pk.HIGHEST_PROTOCOL)
                pass
        print('Completed {} CIK from script {}'.format(count, search_query['part']))
        links = []
    else:
        print("Engine hasn't been defined yet.")
    # search_results = driver.find_element_by_xpath("//html/body/div[@id='main']/div[@id='cnt']/div[@class='mw']/div[@id='rcnt']/div[@class='col']/div[@id='center_col']/div[@id='res']/div[@id='search']//div[@id='ires']/div[@id='rso']/div[@class='bkWMgd']/div[@class='srg']/div[@class='g']")#/div[@class='rc']/div[@class='r']")
    # driver.quit()
    return links


def main():
    driver = setDriver(True)
    search_query = {}
    """ Using the google crawler"""
    # search_query['name'] = "whatever you want to query on google"
    # crawlerWrapper(search_query, 'google', driver)
    """
    Using the SEC CIK 10k engine on one of the CIKs
    """
    # search_query['name'] = '1002910_CIK'
    # search_query['cik'] = '1002910'
    # search_query['dateStart'] = '08/05/2016'
    # search_query['dateEnd'] = '08/05/2019'
    # crawlerWrapper(search_query, 'sec10k')

    """ Using the SEC CIK 10k engine on all of the CIK"""
    # search_query['name'] = "All"
    # search_query['dateStart'] = '08/05/2012'
    # search_query['dateEnd'] = '08/05/2019'
    # crawlerWrapper(search_query, 'sec10kall')

    """ Using the SEC for an SIC"""
    # search_query['dateStart'] = '08/05/2015'
    # search_query['dateEnd'] = '08/05/2019'
    # crawlerWrapper(search_query, 'secsic10k')

    """ site specific search for each company """
    # search_query['url'] = 'https://babahooja.github.io'
    # search_query['url'] = 'https://www.dow.com/en-us/search#t=Products'
    # search_query['name'] = 'dow-products'
    # crawlerWrapper(search_query, 'sitespecific')

    """ Using the TRI for a facility report"""
    # search_query['tri_id'] = '88252JL3GS115SI'
    # crawlerWrapper(search_query, 'tri')

    """ Using the google for subsidiaries"""
    # search_query['name'] = 'samsung'
    # crawlerWrapper(search_query, 'google-subs')

    """ using the cik to get the E-21 of the company / subsidary structure, ultimate parent [top node] """

    # """ Mergers and acquisition """
    # search_query['name'] = "3M Subsidaries"
    # crawlerWrapper(search_query, 'google-subs')
    # search_query['part'] = part_number
    # # starting_point = 1000
    # search_query['starting_point'] = 1000 * (search_query['part'])
    # search_query['ending_point'] = search_query['starting_point'] + 1999
    # crawlerWrapper(search_query, 'everything-all')
if __name__ == "__main__":
    # part_number = int(sys.argv[1])
    # main(part_number)
    main()
