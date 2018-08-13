# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 13:01:07 2018

@author: Melody
"""

from selenium import webdriver
import pickle
import time
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

def get_tri_dict(tri_id, driver):
    url ='https://www3.epa.gov/enviro/facts/tri/ef-facilities/#/Facility/'+tri_id
    driver.get(url)
    time.sleep(1)

    fac_dict = {}
    
    # find tags that contain information
    try:
        fac_name = driver.find_element_by_xpath("//td[@class='ng-binding' and @headers='facName']")
        fac_dict['fac_name'] = fac_name.text
    except:
        fac_dict['fac_name'] = 'NA'

    try:
        tri_id = driver.find_element_by_xpath("//td[@class='ng-binding' and @headers='triID']")
        fac_dict['tri_id'] = tri_id.text
    except:
        fac_dict['tri_id'] = 'NA'

    try:
        address = driver.find_element_by_xpath("//td[@class='ng-binding' and @headers='address']")
        fac_dict['address'] = address.text.replace('\n',' ')
    except:
        fac_dict['address'] = 'NA'

    try:
        frs_id = driver.find_element_by_xpath("//td[@headers='frsID']")
        fac_dict['frs_id'] = frs_id.text
    except:
        fac_dict['frs_id'] = 'NA'

    try:
        mailing_name = driver.find_element_by_xpath("//td[@class='ng-binding' and @headers='mailingName']")
        fac_dict['mailing_name'] = mailing_name.text.replace('\n',' ')
    except:
        fac_dict['mailing_name'] = 'NA'

    try:
        mailing_address = driver.find_element_by_xpath("//td[@class='ng-binding' and @headers='mailingAdd']")
        fac_dict['mailing_address'] = mailing_address.text.replace('\n',' ')
    except:
        fac_dict['mailing_address'] = 'NA'

    try:
        duns_parent_company = driver.find_elements_by_xpath("//td[@class='ng-binding' and @headers='parentCo']")
        for item in duns_parent_company:
            if item.text.isnumeric():
                duns_num = item.text
                fac_dict['duns_num'] = duns_num            
            else:
                parent_company = item.text
                fac_dict['parent_company'] = parent_company
    except:
        fac_dict['duns_num'] = 'NA'
        fac_dict['parent_company'] = 'NA'

    try:
        county = driver.find_element_by_xpath("//td[@class='ng-binding' and @headers='county']")
        fac_dict['county'] = county.text
    except:
        fac_dict['county'] = 'NA'

    try:
        pub_contact = driver.find_element_by_xpath("//td[@class='ng-binding' and @headers='pubContact']")
        fac_dict['pub_contact'] = pub_contact.text 
    except:
        fac_dict['pub_contact'] = 'NA'

    try:
        region = driver.find_element_by_xpath("//td[@class='ng-binding' and @headers='region']")
        fac_dict['region'] = region.text
    except:
        fac_dict['region'] = 'NA'

    try:
        phone = driver.find_element_by_xpath("//td[@class='ng-binding' and @headers='phone']")
        fac_dict['phone'] = phone.text
    except:
        fac_dict['phone'] = 'NA' 

    try:
        latitude = driver.find_element_by_xpath("//td[@class='ng-binding' and @headers='lat']")
        fac_dict['latitude'] = latitude.text
    except:
        fac_dict['latitude'] = 'NA'


    try:
        tribe = driver.find_element_by_xpath("//td[@class='ng-binding' and @headers='tribe']")
        fac_dict['tribe'] = tribe.text
    except:
        fac_dict['tribe'] = 'NA'

    try:
        longitude = driver.find_element_by_xpath("//td[@class='ng-binding' and @headers='lon']")
        fac_dict['longitude'] = longitude.text
    except:
        fac_dict['longitude'] ='NA'

    try:    
        bia_tribal_code = driver.find_element_by_xpath("//td[@class='ng-binding' and @headers='biTribalCode']")
        fac_dict['bia_tribal_code'] = bia_tribal_code.text
    except:
        fac_dict['bia_tribal_code'] = 'NA'

    try:
        naics_sic_lstform = driver.find_elements_by_xpath("//td[@class='ng-binding' and @headers='lstfrm']")
        for i in range(len(naics_sic_lstform)):        
            if i == 0:
                fac_dict['naics'] = numeric_only(naics_sic_lstform[i].text)
            elif i == 1:
                fac_dict['sic'] = numeric_only(naics_sic_lstform[i].text)
            elif i == 2:
                fac_dict['last_form'] = naics_sic_lstform[i].text
    except:
        fac_dict['naics'] = 'NA'
        fac_dict['sic'] = 'NA'
        fac_dict['last_form'] = 'NA'
    return fac_dict


if __name__ == "__main__":
    driver = setDriver()
    # example tri id: 46402SSGRYONENO, 89319BHPCP7MILE, 70070MNSNTRIVER
    tri_id = input('Please enter tri id: ')
    print(get_tri_dict(tri_id,driver))
    # example output
    #{'fac_name': 'USS GARY WORKS', 'tri_id': '46402SSGRYONENO', 'address': '1 N BROADWAY GARY, IN, 46402', 'frs_id': '110000398374', 'mailing_name': 'USS GARY WORKS', 'mailing_address': '1 N BROADWAY MS 70-A GARY, IN, 46402', 'duns_num': '029990699', 'parent_company': 'US STEEL CORP', 'county': 'LAKE', 'pub_contact': 'MEGHAN COX', 'region': '5', 'phone': '(412) 433-6777', 'latitude': '41.616667', 'tribe': 'NA', 'longitude': '-87.3125', 'bia_tribal_code': 'NA', 'naics': 'NA', 'sic': 'NA', 'last_form': 'NA'}