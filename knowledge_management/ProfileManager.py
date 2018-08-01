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
        
    def __iter__(self, instances=1, iam = 1):
        if instances == 1:
            for cik in self.cik_name:
                yield self.get(cik)
        else:
            for i in range(len(self.cik_name)):
                if i % instances == iam:
                    yield self.get(list(self.cik_name.keys())[i])
        
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
                            
    def convert_to_corpus(self, doc):
        ps = PorterStemmer()  
        lmtzr = WordNetLemmatizer()
        text = re.sub('[^A-Za-z]+', ' ', re.sub('\S*@\S*\s?', "", doc.lower())).splitlines()
        doc_list = []
        for line in text:
            words = line.split()
            for word in words:
                doc_list.append(ps.stem(lmtzr.lemmatize(word.strip())))
        return doc_list
        
    def get_docs_by_sentence(self, instances, iam):
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
        
    def get_TaggedDocuments(self, instances, iam):
        good = []
        bad = []
        idk = []
        count = 0
        with open(os.path.join("../data/profilemanager/data", "names.json"), "r") as handle:
            names = json.loads(handle.read())
        with open(os.path.join("../data/profilemanager/data", "cas_from_wiki.json"), "r") as handle:
            cas = json.loads(handle.read())
        goodlist = stem_and_lemmatize(names + cas)
        for text, tag in self.get_docs_by_sentence(instances, iam):
            text = self.convert_to_corpus(str(text))
            tagged = False
            for word in ['call', 'pursuant', 'accord', 'secur', 'goodwil', 'admiss', 'registr', 'amend', 'transit', 'proxi', 'stockhold', 'disclosur', 'mission', 'share', 'flow', 'amortiz', 'pension', 'depreci', 'statement', 'certif', 'reciev', 'payabl', 'licens', 'expens', "jurisdict", ]:
                if not tagged and word in text or len(text) < 3:
                    tagged = True
                    bad.append(TaggedDocument(words=text, tags=list({tag, "bad"})))
            if not tagged:
                for word in goodlist:
                    if not tagged and word in text:
                        tagged = True
                        good.append(TaggedDocument(words=text, tags=list({tag, "good"})))
            if not tagged:
                idk.append(TaggedDocument(words=text, tags=list({tag})))
            count = count + 1
            if count % 100000 == 0:
                if self.rel_path == None:
                    file = open("data/profilemanager/TaggedDocuments/{}_{}_{}.json".format("good_sentences", iam, count//100000), "w")
                    file.write(json.dumps(good, sort_keys = True, indent = 4))
                    file.close()
                    file = open("data/profilemanager/TaggedDocuments/{}_{}_{}.json".format("bad_sentences", iam, count//100000), "w")
                    file.write(json.dumps(bad, sort_keys = True, indent = 4))
                    file.close()
                    file = open("data/profilemanager/TaggedDocuments/{}_{}_{}.json".format("idk_sentences", iam, count//100000), "w")
                    file.write(json.dumps(idk, sort_keys = True, indent = 4))
                    file.close()
                else:
                    file = open(os.path.join(self.rel_path, "data/profilemanager/TaggedDocuments/{}_{}_{}.json".format("good_sentences", iam, count//100000)), "w")
                    file.write(json.dumps(good, sort_keys = True, indent = 4)) 
                    file.close()
                    file = open(os.path.join(self.rel_path, "data/profilemanager/TaggedDocuments/{}_{}_{}.json".format("bad_sentences", iam, count//100000)), "w")
                    file.write(json.dumps(bad, sort_keys = True, indent = 4)) 
                    file.close()
                    file = open(os.path.join(self.rel_path, "data/profilemanager/TaggedDocuments/{}_{}_{}.json".format("idk_sentences", iam, count//100000)), "w")
                    file.write(json.dumps(idk, sort_keys = True, indent = 4)) 
                    file.close()
                good = []
                bad = []
                idk = []
    
    def get_texts(self):
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
                
    def get_texts_by_company(self, item):
        item_string = item['cik']
        try:
            if item['ten_ks'] != None:
                for doc in item['ten_ks']:
                    item_string += "\n\n" +  doc['text']
        except KeyError as k:
            pass
        except Exception as e:
            print("{} threw the following exception while yielding 10K text: {}".format(item['cik'], str(e)))
        try:
            if item['eight_ks'] != None:
                for doc in item['eight_ks']:
                    item_string += "\n\n" +  doc['text']
        except KeyError as k:
            pass
        except Exception as e:
            print("{} threw the following exception while yielding 8K text: {}".format(item['cik'], str(e)))
        try:
            item_string += "\n\n" +  str(item['wiki_page'])
        except KeyError as k:
            pass
        except Exception as e:
            print("{} threw the following exception while yielding wiki_page text: {}".format(item['cik'], str(e)))
        return item_string
    
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
    
    def parse_wikipedia(self, parse_list):
        for company in parse_list:
            company = self[company]
            print("...Now parsing {}".format(company['name']))
            (wiki_page, wiki_table) = wikiParser_new(company['name'])
            company['wiki_page'] = wiki_page
            company['wiki_table'] = wiki_table
            self.update_profile(company)
            
    def write_EX21s_to_raw_text(self):
        for item in self:
            if self.rel_path == None:
                if not os.path.exists("data/profilemanager/EX21s/{}".format(item['cik'])):
                    os.makedirs("data/profilemanager/EX21s/{}".format(item['cik']))
                try:
                    for ex21 in item['EX21s']:
                        file = open("data/profilemanager/EX21s/{}/EX21_{}.txt".format(item['cik'], ex21['time_of_filing']), "w+")
                        file.write(tenk['text'])
                        file.close()
                except:
                    pass
            else:
                if not os.path.exists(os.path.join(self.rel_path, "data/profilemanager/EX21s/{}".format(item['cik']))):
                    os.makedirs(os.path.join(self.rel_path, "data/profilemanager/EX21s/{}".format(item['cik'])))
                try:
                    for ex21 in item['EX21s']:
                        file = open(os.path.join(self.rel_path, "data/profilemanager/EX21s/{}/EX21_{}.txt".format(item['cik'], ex21['time_of_filing'])), "w+")
                        file.write(tenk['text'])
                        file.close()
                except:
                    pass
    
    def write_to_raw_text(self):
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
        for i in range(instances):
            wiki_lists[i].append(item['cik'])
    return wiki_lists
    
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
    pm.write_EX21s_to_raw_text()
#    
if __name__ == "__main__" :
    main()