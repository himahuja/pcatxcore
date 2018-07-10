# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 14:10:12 2018

@author: alex
"""
import parser, pickle
from kpm.corpusBuilder import *
from webcrawlAll import crawlerWrapper
from gensim import models
import logging, re

def WC_to_KPM(query_string):
    crawlerWrapper(query_string, "google")
    with open("data/parsedLinks/{}.pk".format(re.sub('[^A-Za-z]+', '', query_string)), "rb") as handle:
        url_list = pickle.load(handle)
    fm = FileManager()
    fm.read_in_from_iterator(parser_iter("test", url_list))
    fm.save(file_name="data/filemanager/{}.json".format(re.sub('[^A-Za-z]+', '', query_string)))
#    cb = corpusBuilder(file_manager=fm)
#    cb.save()
#    docs = cb.to_TaggedDocument()
#    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
#    model = models.Doc2Vec(docs, workers=3, min_count=20)
#    print("Start training process...")
#    model.train(docs, total_examples=model.corpus_count, epochs=model.iter)
#    print(model.wv.most_similar(positive=['woman', 'king'], negative=['man']))
#    print(model.wv.doesnt_match("breakfast cereal dinner lunch".split()))
#    print(model.wv.similarity('woman', 'man'))

def main():
    with open("data/praedicat_data/Companies.txt") as f:
        content = f.readlines()
    descr = json.loads(open("data/praedicat_data/naics2017_to_naics2017_title.json", "r").read())
    
    for line in content:
        for elem in descr.values():
            query = line + " " + elem
            print("Currently web crawling: {}".format(query))
            WC_to_KPM(query)
    
if __name__ == "__main__" :
    main()