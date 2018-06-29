# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 13:09:11 2018

@author: amichels
"""
import json

class Mapper(object):
    
    def __init__(self, file=None):
        if (file != None):
            try:
                self.mapping = json.loads(open(file).read())
            except Exception as e:
                self.mapping = {}
                print("THERE WAS AN ERROR IN LOADING {}".format(file))
                print(e)
        else:
            self.mapping = {}
            
    #get the aliases (list of strings) from the ID number by [] operators
    def __getitem__(self, id):
        return(self.mapping[id])
            
    def __repr__(self):
        return json.dumps(self.mapping, sort_keys = True, indent = 4)
            
    def __str__(self):
        return json.dumps(self.mapping, sort_keys = True, indent = 4)
        
    #get the aliases (list of strings) from the ID number
    def get(self, id):
        return(self.mapping[id])
    
    #get the aliases (list of strings) from the ID number
    def id_to_alias(self, id):
        return(self.mapping[id])

    
        
        
def main():
    mapper = Mapper(file="KPM/id_to_alias.JSON")
    print(mapper)
    print(mapper["0000001"])
    
    
if __name__ == u"__main__" :
    main()
