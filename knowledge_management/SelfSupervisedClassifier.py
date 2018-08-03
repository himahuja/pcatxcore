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

def get_TaggedDocuments(pm, instances, iam):
        good = []
        bad = []
        idk = []
        count = 0
        numPerList = 1000000
        with open(os.path.join("../data/profilemanager/data", "names.json"), "r") as handle:
            names = json.loads(handle.read())
        with open(os.path.join("../data/profilemanager/data", "cas_from_wiki.json"), "r") as handle:
            cas = json.loads(handle.read())
        templist = [nltk.word_tokenize(word) for word in names] + [nltk.word_tokenize(word) for word in cas]
        goodlist = []
        for wordlist in templist:
            for word in wordlist:
                goodlist.append(word)
        goodlist = goodlist
        for text, tag in pm.get_docs_by_sentence(instances, iam):
            text = convert_to_corpus(str(text))
            tagged = False
            for word in ['call', 'pursuant', 'accord', 'security', 'goodwill', 'registrant', 'amendment', 'transit', 'proxy', 'stockholder', 'disclosure', 'mission', 'share', 'flow', 'amortize', 'pension', 'depreciate', 'statement', 'certify', 'recieviable', 'payable', 'license', 'expense', "jurisdiction" ]:
                if not tagged and word in text or len(text) < 3:
                    tagged = True
                    bad.append(TaggedDocument(words=text, tags=list({tag, "bad"})))
            if not tagged:
                for word in goodlist:
                    if not tagged and word in text:
                        tagged = True
                        good.append(TaggedDocument(words=text, tags=list({tag, "good"})))
            if not tagged:
                idk.append(TaggedDocument(words=text, tags=list({tag})))
            count = count + 1
            if count % numPerList == 0:
                if self.rel_path == None:
                    file = open("../data/profilemanager/TaggedDocuments/{}_{}_{}.json".format("good_sentences", iam, count//numPerList), "w")
                    file.write(json.dumps(good, sort_keys = True, indent = 4))
                    file.close()
                    file = open("../data/profilemanager/TaggedDocuments/{}_{}_{}.json".format("bad_sentences", iam, count//numPerList), "w")
                    file.write(json.dumps(bad, sort_keys = True, indent = 4))
                    file.close()
                    file = open("../data/profilemanager/TaggedDocuments/{}_{}_{}.json".format("idk_sentences", iam, count//numPerList), "w")
                    file.write(json.dumps(idk, sort_keys = True, indent = 4))
                    file.close()
                good = []
                bad = []
                idk = []
                
def tag_idks(instances):
    model = Doc2Vec.load("../data/doc2vec_model")
    good_list = []
    bad_list = []
    i = 0
    for file in os.listdir("../data/profilemanager/TaggedDocuments"):
        filename = os.fsdecode(file)
        if filename.endswith(".json") and "idk_sentences" in filename:
            file = json.loads(open(os.path.join("../data/profilemanager",filename), "r").read())
            for td in file:
                bad = model.docvecs.similarity('bad',td[1][0])
                good = model.docvecs.similarity('good',td[1][0])
                if good/bad >= 1:
                    td[1].append('good')
                    good_list.append(TaggedDocument(words=td[0], tags=td[1]))
                else:
                    td[1].append('bad')
                    bad_list.append(TaggedDocument(words=td[0], tags=td[1]))
            file = open("../data/profilemanager/labeled_good_{}.json".format(filename), "w")
            file.write(json.dumps(good_list, sort_keys = True, indent = 4))
            file.close()
            file = open("../data/profilemanager/labeled_bad_{}.json".format(filename), "w")
            file.write(json.dumps(bad_list, sort_keys = True, indent = 4))
            file.close()

def train_model():           
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
                model = Doc2Vec(docs, workers=7, vector_size=1000)
                print("Start training process...")
                model.train(docs, total_examples=model.corpus_count, epochs=model.iter)
                #save model
                model.save("../data/doc2vec_model")

def main():
    pm = ProfileManager("..")
    get_TaggedDocuments(pm, 6, 5)
    time.sleep(3600)
    train_model()
    tag_idks(6)

if __name__ == "__main__" :
    main()