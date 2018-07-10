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
    fm.save(file_name="data/filemanager/{}.json".format(re.sub('[^A-Za-z0]+', '', query_string)))
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
    
    for line in content:
        query = line.strip()
        print("Currently web crawling: {}".format(query))
        WC_to_KPM(query)
    fm = FileManager()
    for file in os.listdir("data/filemanager"):
        tmp = FileManager()
        tmp.load(os.path.join("data/filemanager", file))
        fm.absorb_file_manager(tmp)
    fm.save()
    fm.train_classifier()
    fm.rank_by_relevance()
    fm.save()
    
if __name__ == "__main__" :
    main()