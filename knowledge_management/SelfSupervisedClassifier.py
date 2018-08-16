# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 20:24:15 2018

@author: alex
"""
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import logging, sys, time
sys.path.append("..")
from knowledge_management.ProfileManager import *
from knowledge_management.WebResourceManager import *

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def convert_to_corpus(doc):
    ps = PorterStemmer()  
    lmtzr = WordNetLemmatizer()
    text = re.sub("[^A-Za-z0-9'-]+", ' ', re.sub('\S*@\S*\s?', "", doc.lower())).splitlines()
    doc_list = []
    for line in text:
        words = line.split()
        for word in words:
            doc_list.append(ps.stem(lmtzr.lemmatize(word.strip())))
    return doc_list

def get_TaggedDocuments(manager):
        bad = []
        idk = []
        count = 0
        numPerList = 1000000
        for item in manager:
            try:
                tagged = False
                sent_list = nltk.sent_tokenize(item['text'])
                for i in range(len(sent_list)):
                    words = sent_list[i].split()
                    tag = "{:06d}{:4d}".format(count, i)
                    letters_in_sentence = sum([len(w) for w in words])
                    if letters_in_sentence > 750 or letters_in_sentence < 50:
                        tagged = True
                        bad.append(TaggedDocument(words=convert_to_corpus(str(sent_list[i])), tags=list({tag, "bad"})))
                    if not tagged:
                        for word in ['skip to main content',  'remember my device', "toggle menu", "user agreement" "privacy statement", "terms of service", "javascript", "footer", "header", "subscribe",  "contact us", "usage has been flagged"]:
                            if not tagged and word in sent_list[i] or len(sent_list[i]) < 3:
                                tagged = True
                                bad.append(TaggedDocument(words=convert_to_corpus(str(sent_list[i])), tags=list({tag, "bad"})))
                    if not tagged:
                        idk.append(TaggedDocument(words=convert_to_corpus(str(sent_list[i])), tags=list({tag})))
                    count = count + 1
                    if count % numPerList == 0:
                        file = open("../data/TaggedDocuments/Labeled/{}_{}.json".format("bad_sentences", count//numPerList), "w")
                        file.write(json.dumps(bad, sort_keys = True, indent = 4))
                        file.close()
                        file = open("../data/TaggedDocuments/Labeled/{}_{}.json".format("idk_sentences", count//numPerList), "w")
                        file.write(json.dumps(idk, sort_keys = True, indent = 4))
                        file.close()
                        bad = []
                        idk = []
            except (KeyError, TypeError) as e:
                print(str(e))
                
        file = open("../data/TaggedDocuments/Labeled/{}_{}.json".format("bad_sentences",count//numPerList), "w")
        file.write(json.dumps(bad, sort_keys = True, indent = 4))
        file.close()
        file = open("../data/TaggedDocuments/Labeled/{}_{}.json".format("idk_sentences",  count//numPerList), "w")
        file.write(json.dumps(idk, sort_keys = True, indent = 4))
        file.close()

def train_model():           
    docs = []
    for file in os.listdir("../data/TaggedDocuments/Labeled"):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            file = json.loads(open(os.path.join("../data/TaggedDocuments/Labeled", filename), "r").read())
            for td in file:
                docs.append(TaggedDocument(words=td[0], tags=[x for x in td[1]]))
    try:
        model = Doc2Vec.load("../data/doc2vec_model")

    except:
        model = Doc2Vec(docs, workers=7, vector_size=1000)
    print("Starting training process...")
    model.train(docs, total_examples=model.corpus_count, epochs=model.iter)
    #save model
    model.save("../data/doc2vec_model")
        

def main():
    for file in os.listdir("../data/webresourcemanagers"):
        wrm = WebResourceManager(rel_path = "..")
        wrm.load(os.path.join("../data/webresourcemanagers", file))
        wrm.rel_path = ".."
        get_TaggedDocuments(wrm)
    train_model()
    for file in os.listdir("../data/webresourcemanagers"):
        wrm = WebResourceManager(rel_path = "..")
        wrm.load(os.path.join("../data/webresourcemanagers", file))
        wrm.rel_path = ".."
        wrm.rank_by_relevance()

if __name__ == "__main__" :
    main()