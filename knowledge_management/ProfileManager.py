#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 12:47:13 2018

@author: alex
"""
import json, os, sys
sys.path.append("..")
from PCATParser import *
import nltk
from gensim.models.doc2vec import TaggedDocument
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import PorterStemmer

class ProfileManager(object):
    
    def __init__(self, rel_path=None):
        """
        Constructor
    
        Sets the **rel_path** variable and reads in various mappings including:
        * CIK (Central Index Key) to name
        * Name to CIK (Central Index Key)
        * Name to (a list of) aliases
        * NAICS (North American Industry Classification System) to description of classification
        * SIC (Standard Industrial Classification) to description of Classification
        * NAICS to SIC
        * SIC to NAICS

    
        Parameters
        ----------
        rel_path : string
            the relative path from the script to the parent folder of where your data will be housed. ProfileManager always assumes that data will be held in "data/profilemanager/data" and profiles will be held in "data/profilemanager/profiles" so this allows you to orient your ProfileManager instance to your data source.
    
        Returns
        -------
        None
    
        """
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
        try:
            if self.rel_path == None:
                self.aliases = json.loads(open("data/profilemanager/data/aliases.json", "r").read())
            else:
                self.aliases = json.loads(open(os.path.join(self.rel_path, "data/profilemanager/data/aliases.json"), "r").read())
        except:
            self.build_aliases()
            self.save_aliases()
        
    def __contains__(self, key):
        """
        Returns true if the instance contains the key
    
        Checks the list of CIK numbers, names, and aliases for matches.

    
        Parameters
        ----------
        key : string
            can be a CIK (Central Index Key) code, name, or alias
    
        Returns
        -------
        bool
            True if found, else False
    
        """
        if key in self.cik_name:
            return True
        elif key in self.name_cik:
            return True
        else:
            for i in range(len(self.aliaseses.values())):
                if alias in self.aliaseses.values()[i]:
                        return True
        return False
    
    def __getitem__(self, key):
        """
        Gets profile identified by the key
  
        Parameters
        ----------
        key : string
            can be a CIK (Central Index Key) code, name, or alias
    
        Returns
        -------
        dict
            A dictionary which is the profile if found, else None
    
        """
        key = key.lower()
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
            for i in range(len(self.name_alias.values())):
                for alias in self.name_alias.values()[i]:
                    if key == alias:
                        if self.rel_path == None:
                            return json.loads(open("data/profilemanager/profiles/{}.json".format(self.name_cik[name_alias.keys()[i]]), "r").read())
                        else:
                            return json.loads(open(os.path.join(self.rel_path, "data/profilemanager/profiles/{}.json".format(self.name_cik[name_alias.keys()[i]])), "r").read())
                        # open name_cik[name_alias.keys()[i]]
        
    def __iter__(self, instances=1, iam = 0):
        """
        An iterator function with the ability to be accessed by multiple instances at once in a safe way.

    
        Parameters
        ----------
        instances : int
            the number of instances using the iterator (default = 1)
        iam : int
            the current instance's assignment [0-*instances*) (default = 0)
    
        Returns
        -------
        dict
            A dictionary which is the profile if found, else None (Yields)
    
        """
        if instances == 1:
            for cik in self.cik_name:
                yield self.get(cik)
        else:
            for i in range(len(self.cik_name)):
                if i % instances == iam:
                    yield self.get(list(self.cik_name.keys())[i])
        
    def __len__(self):
        '''
        Returns the number of CIK (Central Index Key) codes in the instance.
        
        Returns
        -------
        int
            number of CIK (Central Index Key) codes in the instance
        '''
        return len(self.cik_name)
        
    def __repr__(self):
        '''
        Returns a sorted and indented dictionary of CIK (Central Index Key) codes to names of the profiles contained.
        
        Returns
        -------
        string
            a sorted and indented representation of the CIK (Central Index Key) to names map
        '''
        return str(json.dumps(self.cik_name, sort_keys = True, indent = 4))
        
    def __str__(self):
        '''
        Returns a sorted and indented dictionary of CIK (Central Index Key) codes to names of the profiles contained.
        
        Returns
        -------
        string
            a sorted and indented representation of the CIK (Central Index Key) to names map
        '''
        return str(json.dumps(self.cik_name, sort_keys = True, indent = 4))
    
    #def alias_to_cik(self, alias):
    
    def build_aliases(self):
        '''
        Builds an internal list of aliases from the contained items' names and aliases fields.
        
        Returns
        -------
        None
        '''
        self.aliases = []
        for item in self:
            item['name'] = item['name'].lower()
            self.aliases.append(item['name'])
            try:
                for i in range(len(item['alias'])):
                    item['alias'][i] = item['alias'][i].lower()
                    self.aliases.append(item['alias'][i])
            except:
                pass
    
    def cik_to_alias(self, cik):
        """
        Returns a list of aliases of the business entity identified by the CIK (Central Index Key) code.

    
        Parameters
        ----------
        cik : string
            the CIK (Central Index Key) code of a business
    
        Returns
        -------
        list of strings
            a list of aliases associated with the CIK code
    
        """
        return self.name_alias[self.cik_name[cik]]
        
    def cik_to_description(self, cik):
        """
        Returns a list of business activities associated with the CIK code.
        
        Returns a list of descriptions of the industries of the NAICS (North American Industry Classification System) and SIC (Standard Industrial Classification) codes of the business entity identified by the CIK (Central Index Key) code.

    
        Parameters
        ----------
        cik : string
            the CIK (Central Index Key) code of a business
    
        Returns
        -------
        list of strings
            a list of descriptions of business activities associated with the CIK code
    
        """
        return self.naics_description[self.get(cik)['naics']] + self.sic_description[self.get(cik)['sic']]
        
    def cik_to_naics(self, cik):
        """
        Returns the NAICS (North American Industry Classification System) codes of the business entity identified by the CIK (Central Index Key) code.
    
        Parameters
        ----------
        cik : string
            the CIK (Central Index Key) code of a business
    
        Returns
        -------
        list of strings
            the NAICS codes associated with the CIK code
    
        """
        return self.get(cik)['naics']
        
    def cik_to_name(self, cik):
        """
        Returns the name of the business entity identified by the CIK (Central Index Key) code.
    
        Parameters
        ----------
        cik : string
            the CIK (Central Index Key) code of a business
    
        Returns
        -------
        string
            the name associated with the CIK code
    
        """
        return self.cik_name[cik]
    
    def cik_to_sic(self, cik):
        """
        Returns the SIC (Standard Industrial Classification) codes of the business entity identified by the CIK (Central Index Key) code.
    
        Parameters
        ----------
        cik : string
            the CIK (Central Index Key) code of a business
    
        Returns
        -------
        list of strings
            the SIC codes associated with the CIK code
    
        """
        return self.get(cik)['sic']

    def clean_financial_statements(self):
        """
        Removes the text fields of SEC documents in the profiles.
        
        Removes the text field of all ten_k's, eight_k's, and EX21's which are either the empty string or None.
    
    
        Returns
        -------
        None
    
        """
        for company in self:
            if company['ten_ks'] != None:
                for elem in company['ten_ks']:
                    if elem['text'] == "" or elem['text'] == None:
                        del elem['text']
            if company['eight_ks'] != None:
                for elem in company['eight_ks']:
                    if elem['text'] == "" or elem['text'] == None:
                        del elem['text']
            if company['EX21S'] != None:
                for elem in company['EX21s']:
                    if elem['text'] == "" or elem['text'] == None:
                        del elem['text']
                    
    def generate_profiles(self):
        """
        Populates the Profile Manager with profiles.
        
        Currently the code uses two additional JSON files to generate profiles:
        * a map from CIK (Central Index Key) to SIC (Standard Industrial Classification)
        * a map from SIC (Standard Industrial Classification) to NAICS (North American Industrial Classification System)

        The code uses the various mappings to aggregate the information into one profile for each business entity.
    
    
        Returns
        -------
        None
    
        """
        if self.rel_path == None:
            cik_to_sic = json.loads(open("data/profilemanager/data/cik_to_sic.json", "r").read())
            sic_to_naics = json.loads(open("data/profilemanager/data/sic_to_naics.json", "r").read())
        else:
            cik_to_sic = json.loads(open(os.path.join(self.rel_path, "data/profilemanager/data/cik_to_sic.json"), "r").read())
            sic_to_naics = json.loads(open(os.path.join(self.rel_path, "data/profilemanager/data/sic_to_naics.json"), "r").read())
        for cik in self.cik_name:
            this = {}
            this['cik'] = cik
            this['name'] = self.cik_to_name(cik).lower()
            this['sic'] = cik_to_sic[cik]
            try:
                this['naics'] = [ x for x in sic_to_naics[this['sic']] ]
            except:
                this['naics'] = None
            this['subsidiaries'] = None
            this['website'] = None
            self.update_profile(this)
        
    def get(self, key):
        """
        Gets profile identified by the key
  
        Parameters
        ----------
        key : string
            can be a CIK (Central Index Key) code, name, or alias
    
        Returns
        -------
        dict
            A dictionary which is the profile if found, else None
    
        """
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
            for i in range(len(self.name_alias.values())):
                for alias in self.name_alias.values()[i]:
                    if key == alias:
                        if self.rel_path == None:
                            return json.loads(open("data/profilemanager/profiles/{}.json".format(self.name_cik[name_alias.keys()[i]]), "r").read())
                        else:
                            return json.loads(open(os.path.join(self.rel_path, "data/profilemanager/profiles/{}.json".format(self.name_cik[name_alias.keys()[i]])), "r").read())
                        # open name_cik[name_alias.keys()[i]]
    
    def get_aliases(self):
        """
        A getter function for the the list of aliases

        Returns
        -------
        list of strings
            a list of names and aliases of entities in the instance
    
        """
        return self.aliases
        
    def get_docs_by_sentence(self, instances, iam):
        """
        An generator function of the sentences of the documents contained with the ability to be accessed by multiple instances at once in a safe way.

    
        Parameters
        ----------
        instances : int
            the number of instances using the iterator (default = 1)
        iam : int
            the current instance's assignment [0-*instances*) (default = 0)
    
        Returns
        -------
        list of tuples (string, string)
            A list tuples representing the sentences of the documents contained and the IDs of the sentences (Yields)
    
        """
        for item in self.__iter__(instances, iam):
            try:
                if item['ten_ks'] != None:
                    for doc in item['ten_ks']:
                        sent_list = nltk.sent_tokenize(doc['text'])
                        for i in range(len(sent_list)):
                            yield (sent_list[i], str(item['cik'] + "_10k_" + doc['time_of_filing'] + "_" + str(i)))
            except KeyError as k:
                pass
            except Exception as e:
                print("{} threw the following exception while yielding 10K text: {}".format(item['cik'], str(e)))
            try:
                if item['eight_ks'] != None:
                    for doc in item['eight_ks']:
                        sent_list = nltk.sent_tokenize(doc['text'])
                        for i in range(len(sent_list)):
                            yield (sent_list[i], str(item['cik'] + "_8k_" + doc['time_of_filing'] + "_" + str(i)))
            except KeyError as k:
                pass
            except Exception as e:
                print("{} threw the following exception while yielding 8K text: {}".format(item['cik'], str(e)))
            try:
                sent_list = nltk.sent_tokenize(str(item['wiki_page']['text']))
                for i in range(len(sent_list)):
                    yield (sent_list[i], str(item['cik'] + "_wiki_page" + "_" + str(i)))
            except KeyError as k:
                pass
            except Exception as e:
                print("{} threw the following exception while yielding wiki_page text: {}".format(item['cik'], str(e)))

    def get_resources_by_company(self, item):
        """
        A getter for the documents and associated URLs of the resources by company

    
        Parameters
        ----------
        item : dict
            a profile
    
        Returns
        -------
        list of tuples (string, string)
            A list tuples representing the text of the documents contained and the URLs of the documents
    
        """
        resources = []
        try:
            if item['ten_ks'] != None:
                for doc in item['ten_ks']:
                    resources.append((doc['text'], doc['url']))
        except KeyError as k:
            pass
        except Exception as e:
            print("{} threw the following exception while yielding 10K text: {}".format(item['cik'], str(e)))
        try:
            if item['eight_ks'] != None:
                for doc in item['eight_ks']:
                    resources.append((doc['text'], doc['url']))
        except KeyError as k:
            pass
        except Exception as e:
            print("{} threw the following exception while yielding 8K text: {}".format(item['cik'], str(e)))
        return resources
    
    def get_texts(self):
        """
        A getter for the documents contained

    
        Returns
        -------
        list of tuples (string, string)
            A list tuples representing the text of the documents contained and the IDs of the documents (Yields)
    
        """
        for item in self:
            try:
                if item['ten_ks'] != None:
                    for doc in item['ten_ks']:
                        yield (doc['text'], str(item['cik'] + "_10k_" + doc['time_of_filing']))
            except KeyError as k:
                pass
            except Exception as e:
                print("{} threw the following exception while yielding 10K text: {}".format(item['cik'], str(e)))
            try:
                if item['eight_ks'] != None:
                    for doc in item['eight_ks']:
                        yield (doc['text'], str(item['cik'] + "_8k_" + doc['time_of_filing']))
            except KeyError as k:
                pass
            except Exception as e:
                print("{} threw the following exception while yielding 8K text: {}".format(item['cik'], str(e)))
            try:
                yield (item['wiki_page'], str(item['cik'] + "_wiki_page"))
            except KeyError as k:
                pass
            except Exception as e:
                print("{} threw the following exception while yielding wiki_page text: {}".format(item['cik'], str(e)))
    
    def naics_to_description(self, naics):
        """
        Returns a list of descriptions of the industrial code.
        

        Parameters
        ---------
        naics (string)
            is a NAICS (North American Industry Classification System) code.
        
        Returns
        -------
        list of strings
            a list of descriptions of the industrial code.
        
        """
        return self.naics_description[naics]
    
    def naics_to_sic(self, naics):
        """
        Returns the SIC (Standard Industrial Classification) most closely associated with naics.
        

        Parameters
        ---------
        naics (string)
            is a NAICS (North American Industry Classification System) code.
        
        Returns
        -------
        string
           the SIC (Standard Industrial Classification) most closely associated with naics
        
        """
        return self.naics_sic[naics]
    
    def name_to_aliases(self, name):
        """
        Returns a list of aliases of the business entity.
        

        Parameters
        ---------
        name (string)
            the name of a business entity.
        
        Returns
        -------
        list of strings
           a list of aliases associated with the business entity
        
        """
        return self.name_alias[name]
    
    def name_to_cik(self, name):
        """
        Returns the CIK (Central Index Key) of the named business entity.
        

        Parameters
        ---------
        name (string)
            the name of a business entity.
        
        Returns
        -------
        string
           the CIK (Central Index Key) of the named business entity.
        
        """
        return self.name_cik[name]
    
    def name_to_description(self, name):
        """
        Returns a list of descriptions of the industries of the named business entity.
        

        Parameters
        ---------
        name (string)
            the name of a business entity.
        
        Returns
        -------
        list of strings
           a list of descriptions of the industries of the named business entity
        
        """
        return self.naics_description[self.get(name).naics] + self.sic_description[self.get(name).sic]
        
    def parse_sec_docs(self, filename):
        """
        The code parses the filings which haven't already been parsed, iterating on the CIK codes contained in filename. This means if the CIK codes are disjoint, this method can safely be run in parallel.
        

        Parameters
        ---------
        filename (string)
            the name of a JSON file in "data/profilemanager/data/edgardata/JSON". It must be a dictionary from CIK (Central Index Key) to a dictionary containing the keys "10K", "8K", and "EX21". These keys must map to a list of dictionaries each containing the keys "time_of_filing" and "url".
        
        Returns
        -------
        None
        
        """
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
    
    def parse_wikipedia(self, parse_list):
        """
        Gets the information on the Wikipedia pages for the companies in parse_list
        
        Iterates on the companies contained and searching Wikipedia for the name field, then saves the returned page's parsed table and text in dictionaries ("wiki_table" and "wiki_page" respectively). The table is a dictionary from heading to values and the page is a dictionary from section headings to content.
        

        Parameters
        ---------
        parse_list (list of dicts)
            list of profiles which you would like to get the Wikipedia information for
        
        Returns
        -------
        None
        
        """
        for company in parse_list:
            company = self[company]
            print("...Now parsing {}".format(company['name']))
            (wiki_page, wiki_table) = wikiParser_new(company['name'])
            company['wiki_page'] = wiki_page
            company['wiki_table'] = wiki_table
            self.update_profile(company)
            
    def save_aliases(self):
        """
        Saves the aliases list to "profilemanager/data/aliases.json" using rel_path
        

        Returns
        -------
        None
        
        """
        if self.rel_path == None:
            file = open("data/profilemanager/data/aliases.json", "w")
        else:
            file = open(os.path.join(self.rel_path, "data/profilemanager/data/aliases.json"), "w")
        file.write(json.dumps(self.aliases, sort_keys = True, indent = 4))
        file.close()
        
    def update_profile(self, profile):
        """
        Writes the current instance of the profile to the JSON
        

        Parameters
        ---------
        profile (dict)
            profiles which you would like update the saved version of
        
        Returns
        -------
        None
        
        """
        if self.rel_path == None:
            file = open("data/profilemanager/profiles/{}.json".format(profile['cik']), "w")
            file.write(json.dumps(profile, sort_keys = True, indent = 4))
            file.close()
        else:
            file = open(os.path.join(self.rel_path, "data/profilemanager/profiles/{}.json".format(profile['cik'])), "w")
            file.write(json.dumps(profile, sort_keys = True, indent = 4)) 
            file.close()
    
    def write_to_raw_text(self):
        """
        Writes all of the contained documents to "profilemanager/raw_text"
        
        
        Returns
        -------
        None
        
        """
        for item in self:
            if self.rel_path == None:
                if not os.path.exists("data/profilemanager/raw_text/{}".format(item['cik'])):
                    os.makedirs("data/profilemanager/raw_text/{}".format(item['cik']))
                file = open("data/profilemanager/raw_text/{}/wiki_page.txt".format(item['cik']), "w+")
                file.write(json.dumps(item['wiki_page'], sort_keys = True, indent = 4))
                file.close()
                file = open("data/profilemanager/raw_text/{}/wiki_table.txt".format(item['cik']), "w+")
                file.write(json.dumps(item['wiki_table'], sort_keys = True, indent = 4))
                file.close()
                try:
                    for tenk in item['ten_ks']:
                        file = open("data/profilemanager/raw_text/{}/tenk_{}.txt".format(item['cik'], tenk['time_of_filing']), "w+")
                        file.write(tenk['text'])
                        file.close()
                except:
                    pass
                try:
                    for eightk in item['eight_ks']:
                        file = open("data/profilemanager/raw_text/{}/eightk_{}.txt".format(item['cik'], eightk['time_of_filing']), "w+")
                        file.write(eightk['text'])
                        file.close()
                except:
                    pass
            else:
                if not os.path.exists(os.path.join(self.rel_path, "data/profilemanager/raw_text/{}".format(item['cik']))):
                    os.makedirs(os.path.join(self.rel_path, "data/profilemanager/raw_text/{}".format(item['cik'])))
                file = open(os.path.join(self.rel_path, "data/profilemanager/raw_text/{}/wiki_page.txt".format(item['cik'])), "w+")
                file.write(json.dumps(item['wiki_page'], sort_keys = True, indent = 4))
                file.close()
                file = open(os.path.join(self.rel_path, "data/profilemanager/raw_text/{}/wiki_table.txt".format(item['cik'])), "w+")
                file.write(json.dumps(item['wiki_table'], sort_keys = True, indent = 4))
                file.close()
                try:
                    for tenk in item['ten_ks']:
                        file = open(os.path.join(self.rel_path, "data/profilemanager/raw_text/{}/tenk_{}.txt".format(item['cik'], tenk['time_of_filing'])), "w+")
                        file.write(tenk['text'])
                        file.close()
                except:
                    pass
                try:
                    for eightk in item['eight_ks']:
                        file = open(os.path.join(self.rel_path, "data/profilemanager/raw_text/{}/eightk_{}.txt".format(item['cik'], eightk['time_of_filing'])), "w+")
                        file.write(eightk['text'])
                        file.close()
                except:
                    pass
        

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
        for i in range(instances):
            wiki_lists[i].append(item['cik'])
    return wiki_lists
    
def zip_for_stephen(profile_manager, instances, iam):
    my_dict = {}
    for item in profile_manager.__iter__(instances, iam):
        my_dict[item['cik']] = item
    file = open("../data/for_stephen/profiles_part{}".format(str(iam)), "w")
    file.write(json.dumps(my_dict, sort_keys = True, indent = 4))
    file.close()
    
def stem_and_lemmatize(wordlist):
    lmtzr = WordNetLemmatizer()
    ps = PorterStemmer()
    for i in range(len(wordlist)):
        wordlist[i] = ps.stem(lmtzr.lemmatize(wordlist[i]))
        
    return wordlist

def main():
    pm = ProfileManager("..")
#    pm.generate_profiles()
#    wiki_lists = divvy_up_wikipedia(pm,6)
#    pm.parse_wikipedia(wiki_lists[5])
    zip_for_stephen(pm, 5,0)
    zip_for_stephen(pm, 5,1)
    zip_for_stephen(pm, 5,2)
    zip_for_stephen(pm, 5,3)
    zip_for_stephen(pm, 5,4)
#    
if __name__ == "__main__" :
    main()