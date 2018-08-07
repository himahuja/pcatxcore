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
    query = company+"+subsidiaries"
    goog_search = "https://www.google.co.uk/search?q=" + query

    driver.get(goog_search)

    divs = driver.find_elements_by_xpath("//div[@class='kltat']")
    links = driver.find_elements_by_xpath("//a[@class='klitem']")

    sub_dict = {}

    for div,link in zip(divs,links):
        sub_dict[div.text] = link.get_attribute('href')
    return sub_dict

def get_master_dict(name):
    driver = setDriver()
    master_dict = {}
    order = 1
    
    for key in name.keys():
        try:
            company = name[key]
            master_dict[company] = get_sub(company,driver)
            if master_dict[company] == {}:
                del master_dict[company]
            print("...{:.2f}% done, processing link {}".format((order/len(name))*100,order))
            order += 1
        except:
            print('Couldnt find subsidiaries')
            pass

    return master_dict

if __name__ == "__main__":
    
    with open('cikcodes2name.pk', 'rb') as f:
        name = pickle.load(f)

    master_dict = get_master_dict(name)
    
    with open('master_subsidiaries.pk', 'wb') as f:
        pickle.dump(master_dict, f)
    
