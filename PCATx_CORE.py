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
    wrm = WebResourceManager()
    wrm.read_in_docs(parser_iter("test", url_list))
    wrm.save(file_name="data/webresourcemanagers/{}.json".format(re.sub('[^A-Za-z]+', '', query_string)))
#    cb = corpusBuilder(file_manager=wrm)
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
    wrm = WebResourceManager()
    for file in os.listdir("data/webresourcemanagers"):
        tmp = WebResourceManager()
        tmp.load(os.path.join("data/webresourcemanagers", file))
        wrm.absorb_file_manager(tmp)
    wrm.save()
    wrm.train_classifier()
    wrm.rank_by_relevance()
    wrm.save()
    for line in content:
        line = line.strip()
        WC_to_KPM(line)
    
if __name__ == "__main__" :
    main()