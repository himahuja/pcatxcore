# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 18:56:05 2018

@author: alex
"""
import codecs, json, os, re

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

def read_in_dicts_from_txt():
    sic_dict = json.loads(open(os.path.join("../..", "sic_dict.txt")))
    file = open(os.path.join("../../data", "sic_to_description.json"), "w")
    file.write(json.dumps(sic_dict, sort_keys = True, indent = 4))
    file.close()
    naics_dict = json.loads(open(os.path.join("../..", "naics_dict.txt")))
    file = open(os.path.join("../../data", "naics_to_description.json"), "w")
    file.write(json.dumps(naics_dict, sort_keys = True, indent = 4))
    file.close()
    sic_naics_dict = json.loads(open(os.path.join("../..", "sic_naics_dict.txt")))
    file = open(os.path.join("../../data", "sic_to_description.json"), "w")
    file.write(json.dumps(sic_dict, sort_keys = True, indent = 4))
    file.close()

def main():    
    read_in_dicts_from_txt()
    
if __name__ == "__main__" :
    main()
    