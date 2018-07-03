#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


if __name__ == "__main__":
    search_query = ""
    search_query.replace(" ", "+")
    url = "https://chemicalwatch.com/search?q=" + search_query
    driver = webdriver.Chrome()
    driver.get(url)

# GOING TO ADD THE httrack script here for the terminal.
