# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 20:24:15 2018

@author: alex
"""
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import logging, sys, time
sys.path.append("..")
from knowledge_management.ProfileManager import *

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
     
def train_model(instances):           
    docs = []
    for file in os.listdir("../data/profilemanager/TaggedDocuments"):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            file = json.loads(open(os.path.join("../data/profilemanager/TaggedDocuments", filename), "r").read())
            for td in file:
                docs.append(TaggedDocument(words=td[0], tags=list(td[1])))
            try:
                model = Doc2Vec.load("../data/doc2vec_model")
                print("Start training process...")
                model.train(docs, total_examples=model.corpus_count, epochs=model.iter)
                #save model
                model.save("../data/doc2vec_model")
            except:
                model = Doc2Vec(docs, workers=7, vector_size=300)
                print("Start training process...")
                model.train(docs, total_examples=model.corpus_count, epochs=model.iter)
                #save model
                model.save("../data/doc2vec_model")

def tag_idks(instances):
    model = Doc2Vec.load("../data/doc2vec_model")
    good_list = []
    bad_list = []
    for i in range(instances):
        file = json.loads(open("../data/profilemanager/idk_sentences_{}.json".format(str(i)), "r").read())
        for td in file:
            bad = model.docvecs.similarity('bad',td[1][0])
            good = model.docvecs.similarity('good',td[1][0])
            if good/bad >= 1:
                td[1].append('good')
                good_list.append(TaggedDocument(words=td[0], tags=td[1]))
            else:
                td[1].append('bad')
                bad_list.append(TaggedDocument(words=td[0], tags=td[1]))
        file = open("../data/profilemanager/labeled_good_{}.json".format(str(i)), "w")
        file.write(json.dumps(good_list, sort_keys = True, indent = 4))
        file.close()
        file = open("../data/profilemanager/labeled_bad_{}.json".format(str(i)), "w")
        file.write(json.dumps(bad_list, sort_keys = True, indent = 4))
        file.close()

def main():
    pm = ProfileManager("..")
    pm.get_TaggedDocuments(6, 1)
    time.sleep(3600)
    train_model(6)
    tag_idks(6)

if __name__ == "__main__" :
    main()