#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 12:47:13 2018

@author: alex
"""
import json, os, sys
sys.path.append("..")
from PCATParser import *

class ProfileManager(object):
    
    def __init__(self, rel_path=None):
        self.rel_path = rel_path
        if rel_path == None:
            #identify the Profile
            try:
                self.cik_name = json.loads(open("data/profilemanager/data/cik_to_name.json", "r").read())
                self.name_cik = json.loads(open("data/profilemanager/data/name_to_cik.json", "r").read())
                self.name_alias = {}
            except Exception as e:
                print("Error reading in one of the profile indentifier files " + str(e))
            #sic <---> naics transforms
            try:
                self.naics_description = json.loads(open("data/profilemanager/data/naics2017_to_naics2017_title.json", "r").read())
                self.sic_description = json.loads(open("data/profilemanager/data/sic_to_description.json", "r").read())
                self.naics_sic = json.loads(open("data/profilemanager/data/naics_to_sic.json", "r").read())
                self.sic_naics = json.loads(open("data/profilemanager/data/sic_to_naics.json", "r").read())
            except Exception as e:
                print("Error reading in one of the SIC <---> NAICS Transforms " + str(e))
        else:
            #identify the Profile
            try:
                self.cik_name = json.loads(open(os.path.join(self.rel_path, "data/profilemanager/data/cik_to_name.json"), "r").read())
                self.name_cik = json.loads(open(os.path.join(self.rel_path, "data/profilemanager/data/name_to_cik.json"), "r").read())
                self.name_alias = {}
            except Exception as e:
                print("Error reading in one of the profile indentifier files " + str(e))
            #sic <---> naics transforms
            try:
                self.naics_description = json.loads(open(os.path.join(self.rel_path, "data/profilemanager/data/naics2017_to_naics2017_title.json"), "r").read())
                self.sic_description = json.loads(open(os.path.join(self.rel_path, "data/profilemanager/data/sic_to_description.json"), "r").read())
                self.naics_sic = json.loads(open(os.path.join(self.rel_path, "data/profilemanager/data/naics_to_sic.json"), "r").read())
                self.sic_naics = json.loads(open(os.path.join(self.rel_path, "data/profilemanager/data/sic_to_naics.json"), "r").read())
            except Exception as e:
                print("Error reading in one of the SIC <---> NAICS Transforms " + str(e))
        
    def __contains__(self, key):
        if key in self.cik_name:
            return True
        elif key in self.name_cik:
            return True
        else:
            for i in range(len(self.name_aliases.values())):
                if alias in self.name_aliases.values()[i]:
                        return True
        return False
    
    def __getitem__(self, key):
        if key in self.cik_name:
            if self.rel_path == None:
                return json.loads(open("data/profilemanager/profiles/{}.json".format(key), "r").read())
            else:
                return json.loads(open(os.path.join(self.rel_path, "data/profilemanager/profiles/{}.json".format(key)), "r").read())
        elif key in self.name_cik:
            if self.rel_path == None:
                return json.loads(open("data/profilemanager/profiles/{}.json".format(self.name_cik[key]), "r").read())
            else:
                return json.loads(open(os.path.join(self.rel_path, "data/profilemanager/profiles/{}.json".format(self.name_cik[key])), "r").read())
            #open name_cik[key]
        else:
            for i in range(len(self.name_aliases.values())):
                for alias in self.name_aliases.values()[i]:
                    if key == alias:
                        if self.rel_path == None:
                            return json.loads(open("data/profilemanager/profiles/{}.json".format(self.name_cik[name_aliases.keys()[i]]), "r").read())
                        else:
                            return json.loads(open(os.path.join(self.rel_path, "data/profilemanager/profiles/{}.json".format(self.name_cik[name_aliases.keys()[i]])), "r").read())
                        # open name_cik[name_aliases.keys()[i]]
        
    def __iter__(self):
        for cik in self.cik_name:
            yield self.get(cik)
        
    def __len__(self):
        return len(self.cik_name)
        
    def __repr__(self):
        return json.dumps(self.cik_name, sort_keys = True, indent = 4)
        
    def __str__(self):
        return json.dumps(self.cik_name, sort_keys = True, indent = 4)
    
    #def alias_to_cik(self, alias):
    
    def cik_to_alias(self, cik):
        return self.name_alias[self.cik_name[cik]]
        
    def cik_to_description(self, cik):
        return self.naics_description[self.get(cik).naics] + self.sic_description[self.get(cik).sic]
        
    def cik_to_naics(self, cik):
        return self.get(cik)['naics']
        
    def cik_to_name(self, cik):
        return self.cik_name[cik]
    
    def cik_to_sic(self, cik):
        return self.get(cik)['sic']

    def clean_financial_statements(self):
        for company in self:
            if company['ten_ks'] != None:
                for elem in company['ten_ks']:
                    try:
                        del elem['txt']
                    except:
                        pass
                    if elem['text'] == "" or elem['text'] == None:
                        del elem['text']
            if company['eight_ks'] != None:
                for elem in company['eight_ks']:
                    try:
                        del elem['txt']
                    except:
                        pass
                    if elem['text'] == "" or elem['text'] == None:
                        del elem['text']
            if company['EX21S'] != None:
                for elem in company['EX21s']:
                    try:
                        del elem['txt']
                    except:
                        pass
                    if elem['text'] == "" or elem['text'] == None:
                        del elem['text']
                    
    def generate_profiles(self):
        if self.rel_path == None:
            cik_to_sic = json.loads(open("data/profilemanager/data/cik_to_sic.json", "r").read())
            sic_to_naics = json.loads(open("data/profilemanager/data/sic_to_naics.json", "r").read())
        else:
            cik_to_sic = json.loads(open(os.path.join(self.rel_path, "data/profilemanager/data/cik_to_sic.json"), "r").read())
            sic_to_naics = json.loads(open(os.path.join(self.rel_path, "data/profilemanager/data/sic_to_naics.json"), "r").read())
        for cik in self.cik_name:
            this = {}
            this['cik'] = cik
            this['name'] = self.cik_to_name(cik)
            this['sic'] = cik_to_sic[cik]
            try:
                this['naics'] = [ x for x in sic_to_naics[this['sic']] ]
            except:
                this['naics'] = None
            this['subsidiaries'] = None
            this['website'] = None
            self.update_profile(this)
        
    def get(self, key):
        if key in self.cik_name:
            if self.rel_path == None:
                return json.loads(open("data/profilemanager/profiles/{}.json".format(key), "r").read())
            else:
                return json.loads(open(os.path.join(self.rel_path, "data/profilemanager/profiles/{}.json".format(key)), "r").read())
        elif key in self.name_cik:
            if self.rel_path == None:
                return json.loads(open("data/profilemanager/profiles/{}.json".format(self.name_cik[key]), "r").read())
            else:
                return json.loads(open(os.path.join(self.rel_path, "data/profilemanager/profiles/{}.json".format(self.name_cik[key])), "r").read())
            #open name_cik[key]
        else:
            for i in range(len(self.name_aliases.values())):
                for alias in self.name_aliases.values()[i]:
                    if key == alias:
                        if self.rel_path == None:
                            return json.loads(open("data/profilemanager/profiles/{}.json".format(self.name_cik[name_aliases.keys()[i]]), "r").read())
                        else:
                            return json.loads(open(os.path.join(self.rel_path, "data/profilemanager/profiles/{}.json".format(self.name_cik[name_aliases.keys()[i]])), "r").read())
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
        
    def parse_sec_docs(self, filename):
        if self.rel_path == None:
            thicc_edgar = json.loads(open("data/profilemanager/data/edgardata/JSON/{}.json".format(filename), "r").read())
        else:
            thicc_edgar = json.loads(open(os.path.join(self.rel_path, "data/profilemanager/data/edgardata/JSON/{}.json".format(filename)), "r").read())
        for cik in thicc_edgar.keys():
            this = self.get(cik)
            try:
                this['ten_ks'] = thicc_edgar[cik]["10K"]
                remove_queue = []
                for elem in this['ten_ks']:
                    if elem['url'] == "":
                        remove_queue.append(elem)
                for elem in remove_queue:
                    this['ten_ks'].remove(elem)
                if len(this['ten_ks']) == 0:
                    this['ten_ks'] = None
                else:
                    for elem in this['ten_ks']:
                        try:
                            tmp = elem['text']
                        except:
                            elem['text'] = parse_single_page(elem['url'])
            except Exception as e:
                print("{} threw the following exception: {}".format(this['name'], str(e)))
                this['ten_ks'] = None
            try:
                this['eight_ks'] = thicc_edgar[cik]["8K"]
                remove_queue = []
                for elem in this['eight_ks']:
                    if elem['url'] == "":
                        remove_queue.append(elem)
                for elem in remove_queue:
                    this['eight_ks'].remove(elem)
                if len(this['eight_ks']) == 0:
                    this['eight_ks'] = None
                else:
                    for elem in this['eight_ks']:
                        try:
                            tmp = elem['text']
                        except:
                            elem['text'] = eightk_parser(elem['url'])
            except Exception as e:
                this['eight_ks'] = None
            try:
                this['EX21s'] = thicc_edgar[cik]["EX21"]
                remove_queue = []
                for elem in this['EX21s']:
                    if elem['url'] == "":
                        remove_queue.append(elem)
                for elem in remove_queue:
                    this['EX21s'].remove(elem)
                if len(this['EX21s']) == 0:
                    this['EX21s'] = None
                else:
                    for elem in this['EX21s']:
                        try:
                            tmp = elem['text']
                        except:
                            elem['text'] = ex21_parser(elem['url'])
            except Exception as e:
                print("{} threw the following exception: {}".format(this['name'], str(e)))
                this['EX21s'] = None
            self.update_profile(this)
    
    def parse_wikipedia(self):
        for company in self:
            print("...Now parsing {}".format(company['name']))
            (wiki_page, wiki_table) = wikiParser_new(company['name'])
            company['wiki_page'] = wiki_page
            company['wiki_table'] = wiki_table
            self.update_profile(company)
    
    def update_profile(self, profile):
        if self.rel_path == None:
            file = open("data/profilemanager/profiles/{}.json".format(profile['cik']), "w")
            file.write(json.dumps(profile, sort_keys = True, indent = 4))
            file.close()
        else:
            file = open(os.path.join(self.rel_path, "data/profilemanager/profiles/{}.json".format(profile['cik'])), "w")
            file.write(json.dumps(profile, sort_keys = True, indent = 4)) 
            file.close()

def divvy_up_da_thiccedgars(instances, num_edgars):
    mod = num_edgars % instances
    count = 0
    edgar_lists = []
    for i in range(instances):
        edgar_lists.append([])
        if mod == 0:
            for j in range(num_edgars//instances):
                edgar_lists[i].append("bigedgar_part{}".format(count))
                count+=1
        else:
            if i < mod:
                for j in range(num_edgars//instances + 1):
                    edgar_lists[i].append("bigedgar_part{}".format(count))
                    count+=1
            else:
                for j in range(num_edgars//instances):
                    edgar_lists[i].append("bigedgar_part{}".format(count))
                    count+=1
    return edgar_lists
    
def divvy_up_wikipedia(profile_manager, instances):
    wiki_lists = []
    for i in range(instances):
        wiki_lists.append([])
    for item in profile_manager:
        for wiki_list in wiki_lists:
            wiki_list.append(item['cik'])
    return wiki_lists

def main():
    pm = ProfileManager("..")
#    pm.generate_profiles()
    print(divvy_up_wikipedia(pm,6))
#    
if __name__ == "__main__" :
    main()