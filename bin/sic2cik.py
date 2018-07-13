from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# to set the browser options
from selenium.webdriver.chrome.options import Options
# to set the wait time before moving to the next page
from selenium.webdriver.support import expected_conditions as EC
# to save python objects
import pickle as pk
import json, os, re, sys, subprocess
from collections import OrderedDict

def setDriver():
    if sys.platform == 'darwin':
        type_chromedriver = "chromedriver_darwin"
    elif sys.platform == 'linux':
        type_chromedriver = "chromedriver_linux"
    elif sys.platform == 'win32':
        type_chromedriver = "chromedriver_win32.exe"
    path_chromedriver = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", type_chromedriver)
    options = Options()
    # options.add_argument("--headless") # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox') # Bypass OS security model
    options.add_argument('--disable-gpu')  # applicable to windows os only
    options.add_argument('start-maximized') #
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(path_chromedriver, chrome_options=options)
    return driver


def sic2cikCrawler(driver, siccodes2name):
    sic2cik = {}
    cikcodes2name = {}
    ciknames2code = {}
    siccodes2name = OrderedDict(sorted(siccodes2name.items(), key=lambda t: t[0]))
    count = 0
    for sic in siccodes2name.keys():
        count = count + 1
        list_of_cik = []
        start = 0
        while True:
            url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&SIC={}&owner=include&match=&start={}&count=100&hidefilings=0".format(sic.zfill(4), start)
            driver.get(url)
            rows = driver.find_elements_by_xpath('//*[@id="seriesDiv"]/table/tbody/tr[position() >= 2 and position() <= last()]')
            for row in rows:
                col = row.find_elements_by_tag_name("td")
                cikcodes2name[col[0].text] = col[1].text
                ciknames2code[col[1].text] = col[0].text
                list_of_cik.append(col[0].text)
            sic2cik[sic] = list_of_cik
            buttons = driver.find_elements_by_xpath('//*[@id="contentDiv"]/form/input')

            flag = 0

            for button in buttons:
                if button.get_attribute('value') == 'Next 100':
                    start = start + 100
                    flag = 1
                    break
            if flag == 0:
                print("There are no more pages for SIC: {}".format(sic))
                break
        if count%100 == 0:
            print('Saving the first {} items'.format(count))
            with open('../data/SEC_data/sic2cik.pk', 'wb') as handle:
                pk.dump(sic2cik, handle, protocol=pk.HIGHEST_PROTOCOL)

            with open('../data/SEC_data/cikcodes2name.pk', 'wb') as handle:
                pk.dump(cikcodes2name, handle, protocol=pk.HIGHEST_PROTOCOL)

            with open('../data/SEC_data/ciknames2code.pk', 'wb') as handle:
                pk.dump(ciknames2code, handle, protocol=pk.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    driver = setDriver()
    try:
        with open('../data/SEC_data/siccodes2name.pk', 'rb') as f:
            siccodes2name = pk.load(f)
    except:
        print('siccodes2name: file not found!')
    sic2cikCrawler(driver, siccodes2name)
