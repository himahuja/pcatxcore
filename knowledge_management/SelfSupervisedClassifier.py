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

def get_TaggedDocuments_pm(pm, instances, iam):
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
            letters_in_sentence = sum([len(w) for w in text])
            if letters_in_sentence > 750 or letters_in_sentence < 50:
                tagged = True
                bad.append(TaggedDocument(words=text, tags=list({tag, "bad"})))
            if not tagged:
                words = 0
                bad_words = 0
                for word in text:
                    words+= 1
                    if len(word) < 3 or len(word) > 10:
                        bad_words+= 1
                    if bad_words/words >.7:
                        tagged = True
                        bad.append(TaggedDocument(words=text, tags=list({tag, "bad"})))
            if not tagged:
                for word in ['call', 'pursuant', 'accord', 'security', 'goodwill', 'registrant', 'amendment', 'transit', 'proxy', 'stockholder', 'disclosure', 'mission', 'share', 'flow', 'amortize', 'pension', 'depreciate', 'statement', 'certify', 'recieviable', 'payable', 'license', 'expense', "jurisdiction" ]:
                    if not tagged and word in text:
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
                
        file = open("../data/profilemanager/TaggedDocuments/{}_{}_{}.json".format("good_sentences", iam, count//numPerList), "w")
        file.write(json.dumps(good, sort_keys = True, indent = 4))
        file.close()
        file = open("../data/profilemanager/TaggedDocuments/{}_{}_{}.json".format("bad_sentences", iam, count//numPerList), "w")
        file.write(json.dumps(bad, sort_keys = True, indent = 4))
        file.close()
        file = open("../data/profilemanager/TaggedDocuments/{}_{}_{}.json".format("idk_sentences", iam, count//numPerList), "w")
        file.write(json.dumps(idk, sort_keys = True, indent = 4))
        file.close()
        
def get_TaggedDocuments_wrm(manager):
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
                    tag = "{}{:04d}".format(item['id'], i)
                    words = sent_list[i].split()
                    letters_in_sentence = sum([len(w) for w in words])
                    if letters_in_sentence > 750 or letters_in_sentence < 25:
                        tagged = True
                        bad.append(TaggedDocument(words=convert_to_corpus(str(sent_list[i])), tags=list({tag, "bad"})))
                    if not tagged:
                        words = 0
                        bad_words = 0
                        for word in sent_list[i]:
                            words+= 1
                            if len(word) < 3 or len(word) > 10:
                                bad_words+= 1
                            if bad_words/words >.9:
                                tagged = True
                                bad.append(TaggedDocument(words=sent_list[i], tags=list({tag, "bad"})))
                    if not tagged:
                        for word in [ '|', 'skip to main content',  'remember my device', "toggle menu", "user agreement" "privacy statement", "terms of service", "javascript", "footer", "header", "subscribe",  "contact us", "usage has been flagged"]:
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
                
def tag_idks_pm():
    model = Doc2Vec.load("../data/profilemanager/doc2vec_model")
    output = []
    i = 0
    for file in os.listdir("../data/profilemanager/TaggedDocuments"):
        filename = os.fsdecode(file)
        if filename.endswith(".json") and "idk_sentences" in filename:
            file = json.loads(open(os.path.join("../data/profilemanager/TaggedDocuments",filename), "r").read())
            for td in file:
                try:
                    bad = model.docvecs.similarity('bad',td[1][0])
                    good = model.docvecs.similarity('good',td[1][0])
                    output.append([good/bad - 1, td[0]])
                except Exception as e:
                    print("Exception during {}: {}".format(td[1][0], str(e)))
            file = open("../data/profilemanager/output_{}".format(filename), "w")
            file.write(json.dumps(output, sort_keys = True, indent = 4))
            file.close()
            
def tag_idks_wrm():
    model = Doc2Vec.load("../data/doc2vec_model")
    output = []
    i = 0
    for file in os.listdir("../data/TaggedDocuments/Labeled"):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            file = json.loads(open(os.path.join("../data/TaggedDocuments/Labeled",filename), "r").read())
            for td in file:
                try:
                    bad = model.docvecs.similarity('bad',td[1][0])
                    output.append([1/bad, td[0]])
                except Exception as e:
                    print("Exception during {}: {}".format(td[1][0], str(e)))
            file = open("../data/TaggedDocuments/Classified/output_{}".format(filename), "w")
            file.write(json.dumps(output, sort_keys = True, indent = 4))
            file.close()

def train_model_pm():           
    docs = []
    for file in os.listdir("../data/profilemanager/TaggedDocuments"):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            file = json.loads(open(os.path.join("../data/profilemanager/TaggedDocuments", filename), "r").read())
            for td in file:
                docs.append(TaggedDocument(words=td[0], tags=[x for x in td[1]]))
    model = Doc2Vec(docs, workers=7, vector_size=1000)
    print("Start training process...")
    model.train(docs, total_examples=model.corpus_count, epochs=model.iter)
    #save model
    model.save("../data/profilemanager/doc2vec_model")
    
def train_model_wrm():           
    docs = []
    for file in os.listdir("../data/TaggedDocuments/Labeled"):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            file = json.loads(open(os.path.join("../data/TaggedDocuments/Labeled", filename), "r").read())
            for td in file:
                docs.append(TaggedDocument(words=td[0], tags=[x for x in td[1]]))
    model = Doc2Vec(docs, workers=7, vector_size=1000)
    print("Start training process...")
    model.train(docs, total_examples=model.corpus_count, epochs=model.iter)
    #save model
    model.save("../data/doc2vec_model")

def main():
    wrm = WebResourceManager("..")
    for file in os.listdir("../data/webresourcemanagers"):
        tmp = WebResourceManager()
        tmp.load(os.path.join("../data/webresourcemanagers", file))
        tmp.rel_path = ".."
        wrm.absorb_file_manager(tmp)
    get_TaggedDocuments_wrm(wrm)
    train_model_wrm()
    tag_idks_wrm()
#    pm = ProfileManager("..")
#    get_TaggedDocuments_pm(pm, 6, 5)
#    time.sleep(300)
#    train_model_pm()
#    tag_idks_pm()

if __name__ == "__main__" :
    main()