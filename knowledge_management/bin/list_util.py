# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 16:33:20 2018

@author: amichels
"""

from nltk.stem import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer

lmtzr = WordNetLemmatizer()
ps = PorterStemmer()

def stem_and_lemmatize(goodlist, badlist):
    
    for i in range(len(badlist)):
        badlist[i] = ps.stem(lmtzr.lemmatize(badlist[i]))
        
    for i in range(len(goodlist)):
        goodlist[i] = ps.stem(lmtzr.lemmatize(goodlist[i]))
        
    return (goodlist, badlist)
    
def main():
    badlist= ['call', 'pursuant', 'accordance', 'securities', 'admission', 'registrant', 'amendment', 'transition', 'proxy', 'stockholder', 'disclosure', 'mission', 'shares', 'flow', 'amortiz', 'pension', 'depreciation', 'statement', 'certificate', 'recievable', 'payable', 'license', 'expense']
#    goodlist = ['activities', 'subsidiaries', 'segment', 'manufactur', 'produce', 'product', 'sell', 'acquir', 'merge', 'competit', 'chemical', 'hazard']
    with open(os.path.join("../../data/profilemanager/data", "names.json"), "r") as handle:
         names = json.loads(handle.read())
    with open(os.path.join("../../data/profilemanager/data", "cas_from_wiki.json"), "r") as handle:
         cas = json.loads(handle.read())
    goodlist = names + cas
    print(stem_and_lemmatize(goodlist, badlist))
    
if __name__ == "__main__" :
    main()