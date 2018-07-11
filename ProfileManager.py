#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 12:47:13 2018

@author: alex
"""

class Profile(object):
    
    def __init__(self, file_name):
        this = json.loads(open(file_name, "r").read())
        self.name = this['name']
        self.10k = this['10k']
        self.cik = this['cik']
        self.naics = this['naics']
        self.sic = this['sic']
        self.subsidiaries = this['subsidiaries']
        self.website = this['website']