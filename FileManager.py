# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 15:27:52 2018

@author: alex
"""
from parser import *
import json, uuid

class FileManager(object):
    
    def __init__(self):
        #read in the file
        pass
    
    def string_to_uuid(self, string):
        return uuid.uuid5(uuid.NAMESPACE_DNS, string)
    
    def process_list_of_docs(self, list_of_docs):
        for i in range(len(list_of_docs)):
            list_of_docs[i]['id'] = str(self.string_to_uuid(list_of_docs[i]['url']))
            try:
                html = list_of_docs[i]['html']
                file = open(os.path.join("data/source", list_of_docs[i]['id'] +".html"), "w")
                file.write(html.decode('utf-8', 'ignore'))
                file.close()
                del list_of_docs[i]['html']
            except:
                pdf = list_of_docs[i]['pdf']
                file = open(os.path.join("data/source", list_of_docs[i]['id'] +".pdf"), "w")
                file.write(pdf.decode('utf-8', 'ignore'))
                file.close()
                del list_of_docs[i]['pdf']
            file = open(os.path.join("data/sentences", list_of_docs[i]['id']+".json"), "w")
            file.write(json.dumps(list_of_docs[i], sort_keys=True, indent=4))
            file.close()
                
            
        
def main():
    with open("kpm/data/articles.txt") as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    fm = FileManager()
    fm.process_list_of_docs(parser_to_FM("test", content))
    
if __name__ == "__main__" :
    main()