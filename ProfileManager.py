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

class ProfileManager(object):
    
    def __init__(self):
        #identify the Profile
        self.cik_name = {}
        self.name_cik = {}
        self.name_alias = {}
        #sic <---> naics transforms
        self.naics_description = {}
        self.sic_description = {}
        self.naics_sic = {}
        self.sic_naics = {}
        
    def __contains__(self, key):
        if key in self.cik_name:
            return True
        elif key in self.name_cik:
            return True
        else:
            for i in range(len(self.name_aliases.values())):
                for alias in self.name_aliases.values()[i]:
                    if key == alias:
                        return True
    
    def __getitem(self, key):
        if key in self.cik_name:
            #open this file, we have cik
        elif key in self.name_cik:
            #open name_cik[key]
        else:
            for i in range(len(self.name_aliases.values())):
                for alias in self.name_aliases.values()[i]:
                    if key == alias:
                        # open name_cik[name_aliases.keys()[i]]
        
    def __iter__(self):
        for cik in self.cik_name.keys():
            #open the profile
        
    def __len__(self):
        return len(self.cik_name)
        
    def __repr__(self):
        return json.dumps(self.cik_name, sort_keys = True, indent = 4)
        
    def __str__(self):
        return json.dumps(self.cik_name, sort_keys = True, indent = 4)
    
    #def alias_to_cik(self, alias):
    
    def cik_to_alias(self, cik):
        return self.name_alias[self.cik_name[cik]]
        
    def cik_to_naics(self, cik):
        return self.get(cik).naics
    
    def cik_to_sic(self, cik):
        return self.cik_sic[cik]
        
    def cik_to_description(self, cik):
        return self.naics_description[self.get(cik).naics] + self.sic_description[self.get(cik).sic]
        
    def cik_to_name(self, cik):
        return self.cik_name[cik]
        
    def get(self, key):
        if key in self.cik_name:
            #open this file, we have cik
        elif key in self.name_cik:
            #open name_cik[key]
        else:
            for i in range(len(self.name_aliases.values())):
                for alias in self.name_aliases.values()[i]:
                    if key == alias:
                        # open name_cik[name_aliases.keys()[i]]
    
    def naics_to_description(self, naics):
        return self.naics_description[naics]
    
    def naics_to_sic(self, naics):
        return self.naics_sic[naics]
    
    def name_to_aliases(self, name):
        return self.name_alias[name]
    
    def name_to_cik(self, name):
        return self.name_cik[name]
    
    def name_to_description(self, name):
        return self.naics_description[self.get(name).naics] + self.sic_description[self.get(name).sic]