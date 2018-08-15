# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 18:56:05 2018

@author: alex
"""
import codecs, json, os, pickle, re, sys
sys.path.append("../..")
from knowledge_management.WebResourceManager import *

def ProcessAbstracts(dirname):
    for fname in os.listdir(dirname):
        file = codecs.open(os.path.join(dirname, fname), "r+",encoding='utf-8', errors='ignore')
        text = file.read()
        text = text.replace("### abstract ###", "").replace("### introduction ###", "").replace("CITATION", "")
        file.seek(0)
        file.write(text)
        file.truncate()
        file.close()
        if (os.listdir(dirname).index(fname) != 0 and os.listdir(dirname).index(fname) % 100 == 99):
            print("...{:.2f}% done, processing document {} of {}".format(((os.listdir(dirname).index(fname)+1)/len(os.listdir(dirname)))*100,os.listdir(dirname).index(fname)+1,len(os.listdir(dirname))))
    print("...{:.2f}% done, processing document {} of {}".format(100,len(os.listdir(dirname)),len(os.listdir(dirname))))

def Process20NewsGroups(dirname):
    for fname in os.listdir(dirname):
        file = codecs.open(os.path.join(dirname, fname), "r+",encoding='utf-8', errors='ignore')
        text = file.read()
        text = text[text.find("Lines:"):]
        text = text[text.find("\n"):]
        file.seek(0)
        file.write(text)
        file.truncate()
        file.close()
        if (os.listdir(dirname).index(fname) != 0 and os.listdir(dirname).index(fname) % 100 == 99):
            print("...{:.2f}% done, processing document {} of {}".format(((os.listdir(dirname).index(fname)+1)/len(os.listdir(dirname)))*100,os.listdir(dirname).index(fname)+1,len(os.listdir(dirname))))
    print("...{:.2f}% done, processing document {} of {}".format(100,len(os.listdir(dirname)),len(os.listdir(dirname))))
    
def ProcessPipeDelineated(file_in, file_out):
    dictionary = {}
    for line in codecs.open(file_in, "r",encoding='utf-8', errors='ignore').read().splitlines():
        dictionary[line[:line.find("|")]] = line[line.find("|")+1:].strip()
    open(file_out, "w").write(json.dumps(dictionary, sort_keys = True, indent = 4))
    
def TxtToJson(file_in, file_out):
    dictionary = {}
    for line in codecs.open(file_in, "r",encoding='utf-8', errors='ignore').read().splitlines():
        dictionary[line.strip().lower()] = line.strip().lower()
    open(file_out, "w").write(json.dumps(dictionary, sort_keys = True, indent = 4))

def pickle_to_JSON(filename):
#    with open(os.path.join("../../Dictionaries", "naics_dict.pk"), "rb") as handle:
#        file = pickle.load(handle)
#    open(os.path.join("../../data/profilemanager/data", "naics_to_description.json"), "w").write(json.dumps(file, sort_keys = True, indent = 4))
#    with open(os.path.join("../../Dictionaries", "naics_sic_dict.pk"), "rb") as handle:
#        file = pickle.load(handle)
#    open(os.path.join("../../data/profilemanager/data", "naics_to_sic.json"), "w").write(json.dumps(file, sort_keys = True, indent = 4))    
#    with open(os.path.join("../../Dictionaries", "sic_dict.pk"), "rb") as handle:
#        file = pickle.load(handle)
#    open(os.path.join("../../data/profilemanager/data", "sic_to_description.json"), "w").write(json.dumps(file, sort_keys = True, indent = 4))    
#    with open(os.path.join("../../Dictionaries", "sic_naics_dict.pk"), "rb") as handle:
#        file = pickle.load(handle)
#    open(os.path.join("../../data/profilemanager/data", "sic_to_naics.json"), "w").write(json.dumps(file, sort_keys = True, indent = 4))
#     with open(os.path.join("../../data/profilemanager/data", "cikcodes2name.pk"), "rb") as handle:
#         file = pickle.load(handle)
#     open(os.path.join("../../data/profilemanager/data", "cik_to_name.json"), "w").write(json.dumps(file, sort_keys = True, indent = 4)) 
#     with open(os.path.join("../../data/profilemanager/data", "ciknames2code.pk"), "rb") as handle:
#         file = pickle.load(handle)
#     open(os.path.join("../../data/profilemanager/data", "name_to_code.json"), "w").write(json.dumps(file, sort_keys = True, indent = 4)) 
     with open(os.path.join("../../data/profilemanager/data/tridata", "{}.pk".format(filename)), "rb") as handle:
         file = pickle.load(handle)
     open(os.path.join("../../data/profilemanager/data/tridata", "{}.json".format(filename)), "w").write(json.dumps(file, sort_keys = True, indent = 4)) 

def inverse_dictionary():
    this = json.loads(open(os.path.join("../../data/profilemanager/data", "sic_to_cik.json"), "r").read())
    cik_to_sic = {}
    for sic in this:
        for cik in this[sic]:
            try:
                cik_to_sic[cik] = cik_to_sic[cik].append(sic)
            except:
                cik_to_sic[cik] = [sic]
    open(os.path.join("../../data/profilemanager/data", "cik_to_sic.json"), "w").write(json.dumps(cik_to_sic, sort_keys = True, indent = 4))


def names_to_list():
    with open(os.path.join("../../data/profilemanager/data", "target_companies_with_aliases.txt"), "r") as handle:
         file = json.loads(handle.read())
    
    open(os.path.join("../../data/profilemanager/data/names.json"), "w").write(json.dumps(list(file.values()), sort_keys = True, indent = 4))

def lowercase_dat_shit():
    with open(os.path.join("../../data/profilemanager/data", "cik_to_name.json"), "r") as handle:
         file = json.loads(handle.read())
    file = dict((k.lower(), v) for k,v in file.items())
    open(os.path.join("../../data/profilemanager/data/names.json"), "w").write(json.dumps(list(file.values()), sort_keys = True, indent = 4))
    open(os.path.join("../../data/profilemanager/data/cik_to_name.json"), "w").write(json.dumps(file, sort_keys = True, indent = 4))
    with open(os.path.join("../../data/profilemanager/data", "name_to_cik.json"), "r") as handle:
         file = json.loads(handle.read())
    file = dict((k.lower(), v) for k,v in file.items())
    open(os.path.join("../../data/profilemanager/data/name_to_cik.json"), "w").write(json.dumps(file, sort_keys = True, indent = 4))

def csv_to_JSON():
    with open(os.path.join("../../data/praedicat_data", "target_companies_with_aliases.csv"), "r") as handle:
         file = handle.read()
    fout = []
    for line in file.splitlines():
        if len(line) > 4:
            fout.append(line.replace('"', "").replace("'", "").replace("\ufffd", "").strip())
    open(os.path.join("../../data/profilemanager/data/target_companies_with_aliases.json"), "w").write(json.dumps(list(fout), sort_keys = True, indent = 4))

def rename_wrm_files():
    for filename in os.listdir("../../data/docs"):
        if len(filename) > 100:
            file = open("../../data/docs/{}".format(filename), "r+")
            item = json.loads(file.read())
            item['id'] = item['id'][:100]
            new_filename = item['id'] + ".json"
            print("Renaming {} to {}...".format(filename, new_filename))
            for wrm in os.listdir("../../data/webresourcemanagers"):
                wrminstance = WebResourceManager()
                wrminstance.load(os.path.join("../../data/webresourcemanagers", wrm))
                try:
                    del wrminstance.url_to_uuid['url']
                except:
                    pass
                if item['url'] in wrminstance.url_to_uuid:
                    wrminstance.url_to_uuid[item['url']] = item['id']
#            file.seek(0)
#            file.write(json.dumps(item, sort_keys = True, indent = 4))
#            file.truncate()
#            file.close()
            os.rename(os.path.join("../../data/docs", filename), os.path.join("../../data/docs", new_filename))
def main():    
#    pickle_to_JSON("master_dict_portion")
    rename_wrm_files()
    
if __name__ == "__main__" :
    main()
    