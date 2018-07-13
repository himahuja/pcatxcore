"""
Module to parse this list: https://www.sec.gov/info/edgar/siccodes.htm
to find the SIC codes under the SEC.
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# to set the browser options
from selenium.webdriver.chrome.options import Options
# to set the wait time before moving to the next page
from selenium.webdriver.support import expected_conditions as EC
# to save python objects
import pickle as pk

def setDriver():
    options = Options()
    options.add_argument("--headless") # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox') # Bypass OS security model
    options.add_argument('--disable-gpu')  # applicable to windows os only
    options.add_argument('start-maximized') #
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome('/Users/himanshuahuja/Documents/pcatxcore/chromedriver', chrome_options=options)
    return driver

driver = setDriver()
driver.get('https://www.sec.gov/info/edgar/siccodes.htm')

try:
    with open('../data/SEC_data/siccodes2name.pk', 'rb') as f:
        siccodes2name = pk.load(f)
except:
    siccodes2name = {}

try:
    with open('../data/SEC_data/sicnames2code.pk', 'rb') as f:
        sicnames2code = pk.load(f)
except:
    sicnames2code = {}

rows = driver.find_elements_by_xpath("//html/body/table[2]/tbody/tr/td[3]/font/p[4]/table/tbody/tr[position() >= 4 and position() <= last()]")
for row in rows:
    col = row.find_elements_by_tag_name("td")
    siccodes2name[col[0].text] = col[3].text
    sicnames2code[col[3].text] = col[0].text

with open('../data/SEC_data/siccodes2name.pk', 'wb') as handle:
    pk.dump(siccodes2name, handle, protocol=pk.HIGHEST_PROTOCOL)

with open('../data/SEC_data/sicnames2code.pk', 'wb') as handle:
    pk.dump(sicnames2code, handle, protocol=pk.HIGHEST_PROTOCOL)
