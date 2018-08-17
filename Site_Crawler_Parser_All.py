#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 11:38:53 2018

@author: Melody
"""

from selenium import webdriver
import wikipedia as wiki
from bs4 import BeautifulSoup
import json, os, re, sys, subprocess, pickle, time, urllib.request, unicodedata, wikipedia
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import queue


# set driver for all other engines
def setDriver(headless = False):
    if sys.platform == 'darwin':
        type_chromedriver = "chromedriver_darwin"
    elif sys.platform == 'linux':
        type_chromedriver = "chromedriver_linux"
    elif sys.platform == 'win32':
        type_chromedriver = "chromedriver_win32.exe"
    path_chromedriver = os.path.join(os.path.dirname(os.path.realpath(__file__)), type_chromedriver)
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

# get TRI Dictionary
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

# get Google subsidiary
def get_sub(company, driver):
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
    try:
        sub_list.remove(name)
    except:
        pass
    return sub_list

def get_parent_child_dict(company,parent,children_list):
    parent_child_dict = {}
    parent_child_dict['parent'] = parent
    parent_child_dict['children'] = children_list
    return parent_child_dict

def get_recursive_sub(company,driver):
    company_queue = queue.Queue()
    company_queue.put(company)
    master_google_sub = {}
    master_parent_child_dict = {}

    while not company_queue.empty():
        try:
            name = company_queue.get()
            try:
                parent = master_parent_child_dict[name]
            except:
                parent = "NA"
            children_list = get_sub(name,driver)
            try:
                children_list.remove(name)
            except:
                pass
            if children_list != [] and '' not in children_list:
                parent_child_dict = get_parent_child_dict(name,parent,children_list)
                master_google_sub[name] = parent_child_dict
                print(name+' found')
            else:
                continue

            for children in children_list:
                master_parent_child_dict[children] = name
                company_queue.put(children)
        except:
            pass
    return master_google_sub


# EWG ingredient
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

                if not found:
                    print(company+' products attached.')
                    break
            except:
                break
        # map a company to a product list once found
        if prod_list != []:
            comp_prod_dict[company] = prod_list


    except:
        print(company+' not found')

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


            except:
                print(prod+' ingredient not found')

        if prod_ingredient_dict != {}:
            comp_prod_ingredient_dict[key] = prod_ingredient_dict
    return comp_prod_ingredient_dict


# NPIRS
def get_comp_name(text):
    name = ''
    count = 0
    start = False
    stop = False
    for char in text:
        if count == 2:
            return name
        if start:
            name += char
        if char == '\n':
            start = True
            count +=1

def remove_null(comp_list):
    for comp in comp_list:
        if comp == '':
            comp_list.remove('')
    return list(set(comp_list))

def hazard_to_company(chemical,driver):
    try:
        driver.get('http://npirspublic.ceris.purdue.edu/ppis/')
        driver.find_element_by_xpath("//input[@id='ContentPlaceHolder1_active']").click()

        driver.find_element_by_xpath("//input[@id='ContentPlaceHolder1_TextBoxInput2']").send_keys(chemical)

        driver.find_element_by_xpath("//input[@type='submit']").click()
        company = driver.find_element_by_xpath("//input[@type='submit' and @value='Display Companies']")
        chem_info = {}

        company.click()
        pc_code = driver.find_element_by_xpath("//span[@style='color:Black;font-weight:bold;']").text
        chem_name = driver.find_element_by_xpath("//span[@style='color:black;font-weight:bold']").text
        num_companies = driver.find_element_by_xpath("//span[@style='color:Black;font-weight:bold']").text
        td_list = driver.find_element_by_xpath("//table[@width='100%']").find_elements_by_xpath("//td")
        #tbody_list = driver.find_element_by_xpath("//tbody")
        comp_list = []
        for td in td_list:
            if td.find_element_by_xpath("//input[@type='submit' and @value='Display Products']") != []:
                if 'Company Information' not in td.text:
                    comp_list.append(td.text)
        names = ''
        for comp in remove_null(comp_list):
            names += get_comp_name(comp)
        return remove_null(names.split('\n'))
    except:
        print('Unable to find companies for the hazard')
        return []

def wikiParser(company):
    """

    """
    wiki_page = {}
    wiki_table = {}
    try:
        page = wiki.page(title = company)
    except:
        print("Reading the wiki page, {} was not possible".format(company))
        return (wiki_page, wiki_table, "", "", "<ul></ul>")
    secs = page.sections
    for sec in secs:
        wiki_page[sec] = page.section(sec)
    # Do the wikipedia table
    link = page.url
    body = urllib.request.urlopen(link).read()
    soup = BeautifulSoup(body, 'lxml')
    title = soup.find('title')
    if title != None:
        title = str(title).replace("<title>", "").replace("</title>", "").replace("- Wikipedia", "").strip()
    try:
        table = soup.find('table',{'class':'infobox vcard'})
        rows = table.find_all('tr')
        for row in rows:
            right = row.find_all('td')
            left = row.find_all('th')
            for head, elem in zip(left, right):
                filler = unicodedata.normalize("NFKD", head.get_text(strip=True))
                els = elem.find_all('li')
                if len(els) != 0:
                    temp_list = []
                    for el in els:
                        temp_list.append(unicodedata.normalize("NFKD",re.sub('\[[^()]*\]', "", el.get_text(strip=True))))
                    wiki_table[filler] = temp_list
                elif head.text == "Founded":
                    wiki_table[filler] = unicodedata.normalize("NFKD",elem.get_text(strip=True).split(";", 1)[0])
                elif elem.text != "":
                    wiki_table[filler] = unicodedata.normalize("NFKD",re.sub('\[[^()]*\]', "",elem.get_text(strip=True)))
    except:
        print("Wikipedia Table does not exist for {}".format(company))
    return (wiki_page, wiki_table, title, link, table)

if __name__ == "__main__":
    print('Please select an engine:')
    print('1. TRI Facility Information(TRI)')
    print('2. Recursive Google Subsidiaries(GOOGLE)')
    print('3. EWG Skin Deep Cosmetics(EWG)')
    print('4. NPIRS Hazard to Companies(NPIRS)')
    print('5. Wikipedia (WIKI)')

    engine = input("Please enter your choice (TRI/GOOGLE/EWG/NPIRS/WIKI): ")
    engine = engine.lower()

    if engine == 'tri' or engine == "1":
        # example tri id: 46402SSGRYONENO, 89319BHPCP7MILE, 70070MNSNTRIVER
        driver = setDriver()
        tri_id = input('Please enter a tri id: ')
        print(json.dumps(get_tri_dict(tri_id,driver), sort_keys = True, indent = 4))
        driver.quit()
        # example output
        #{'fac_name': 'ROBINSON NEVADA MINING CO', 'tri_id': '89319BHPCP7MILE', 'address': '4232 W WHITE PINE CO RD 44 RUTH, NV, 89319', 'frs_id': '110042080832', 'mailing_name': 'ROBINSON NEVADA MINING CO', 'mailing_address': 'PO BOX 382 RUTH, NV, 89319', 'parent_company': 'NA', 'county': 'WHITE PINE', 'pub_contact': 'AMANDA HILTON', 'region': '9', 'phone': '(775) 289-7045', 'latitude': '39.27083', 'tribe': 'NA', 'longitude': '-115.0125', 'bia_tribal_code': 'NA', 'naics': 'NA', 'sic': 'NA', 'last_form': 'NA'}
    elif engine == 'google' or engine == "2":
        # example company: ABC-MART,INC.
        driver = setDriver()
        company = input('Enter a company name: ')
        master_google_sub = get_recursive_sub(company,driver)
        # print result of all subsidiaries as a list
        print(json.dumps(master_google_sub, sort_keys = True, indent = 4))
        driver.quit()
        # example output:
        #{'ABC-MART,INC.': {'parent': 'NA', 'children': ['ABC-Mart Korea Co,. Ltd', 'LaCrosse Footwear']}, 'LaCrosse Footwear': {'parent': 'ABC-MART,INC.', 'children': ['Danner Inc', "White's Boots", 'LaCrosse Europe ApS', 'Environmentally Neutral Design Outdoor, Inc.', 'LaCrosse Europe Inc', 'LaCrosse International, Inc']}, 'LaCrosse International, Inc': {'parent': 'LaCrosse Footwear', 'children': ['Danner Inc', "White's Boots", 'LaCrosse Europe ApS', 'Environmentally Neutral Design Outdoor, Inc.', 'LaCrosse Europe Inc']}}
    elif engine == 'ewg' or engine == "3":
        # example ewg company name: Advanced Research Laboratories, Advanced Beauty, Inc.
        driver = setDriver()
        company = input('Please enter a company name: ')
        driver = setDriver()
        comp_prod_dict = company_to_product(company,driver)
        print(json.dumps(product_to_ingredient(comp_prod_dict,driver), sort_keys = True, indent = 4))
        driver.quit()
        # example output:
        # {'Advanced Research Laboratories': {'Zero Frizz Keratin Corrective Hair Serum': ['FRAGRANCE', 'OCTINOXATE ETHYLHEXYL METHOXYCINNAMATE', 'TOCOPHERYL ACETATE', 'DIMETHICONE', 'CYCLOMETHICONE', 'KERATIN AMINO ACIDS', 'DIMETHICONOL'], 'Zero Frizz Keratin Smoothing Conditioner': ['FRAGRANCE', 'DMDM HYDANTOIN (FORMALDEHYDE RELEASER)', 'OCTINOXATE ETHYLHEXYL METHOXYCINNAMATE', 'METHYLPARABEN', 'PEG/ PPG-18/ 18 DIMETHICONE', 'CYCLOPENTASILOXANE', 'DIMETHICONE', 'BEHENTRIMONIUM CHLORIDE', 'CETRIMONIUM CHLORIDE', 'PROPYLENE GLYCOL', 'HYDROLYZED KERATIN', 'CITRIC ACID', 'AMODIMETHICONE', 'TRIBUTYL CITRATE', 'STEARAMIDOPROPYL DIMETHYLAMINE', 'CETYL ALCOHOL', 'PANTHENOL', 'HYDROXYETHYLCELLULOSE', 'STEARYL ALCOHOL', 'SODIUM BENZOTRIAZOLYL BUTYLPHENOL SULFONATE', 'DISODIUM EDTA', 'C12-14 ISOPARAFFIN', 'BUTETH-3', 'TRIDECETH-12', 'WATER']}}
    elif engine == 'npirs' or engine == "4":
        # hazards: formaldehyde, glyphosate, arsenic, aluminum, carbaryl
        driver = setDriver()
        name = input("Please enter a hazard name: ")
        comp_list = hazard_to_company(name, driver)
        print(comp_list)
        driver.quit()
    elif engine == 'wiki' or engine == "5":
        # hazards: formaldehyde, glyphosate, arsenic, aluminum, carbaryl
        name = input("Please enter a Wikipedia query: ")
        wiki = wikiParser(name)
        print(json.dumps(wiki[1], indent = 4, sort_keys = True))
        print(json.dumps(wiki[0], indent = 4, sort_keys = True))
