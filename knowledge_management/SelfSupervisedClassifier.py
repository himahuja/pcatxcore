# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 20:24:15 2018

@author: alex
"""
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import logging, sys, time
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
sys.path.append("..")
from knowledge_management.ProfileManager import *
from knowledge_management.WebResourceManager import *


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def convert_to_corpus(doc):
    ps = PorterStemmer()  
    lmtzr = WordNetLemmatizer()
    doc_list = []
    if type(doc) is list:
        for word in doc:
            doc_list.append(ps.stem(lmtzr.lemmatize(re.sub("[^A-Za-z0-9'-]+", '', word.lower()).strip())))
    if type(doc) is str:
        for word in word_tokenize(doc):
            doc_list.append(ps.stem(lmtzr.lemmatize(re.sub("[^A-Za-z0-9'-]+", '', word.lower()).strip())))
    return doc_list
    
def train_tfidf(corpus):
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf.fit_transform(corpus)
        return tfidf
    
def get_relevance_score(tfidf, document):
        response = tfidf.transform([document])
        feature_names = tfidf.get_feature_names()
    
        score_dict = {}
        for col in response.nonzero()[1]:
            score_dict[feature_names[col]] = response[0,col]
    
        word_list = nltk.word_tokenize(document)
        total_score = 0
        count_keywords = 0
        for word in word_list:
            if word in score_dict:
                total_score += score_dict[word]
                count_keywords += 1
        if (count_keywords != 0):   
            score = total_score / count_keywords
        else:
            score = 0
        return score

def train_tfidf_pm():
    training_list = []
    for file in os.listdir("../data/profilemanager/TaggedDocuments/Labeled"):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            file = json.loads(open(os.path.join("../data/profilemanager/TaggedDocuments/Labeled",filename), "r").read())
            for td in file:
                sentence = ""
                for word in td[0]:
                    sentence+=word + " "
                training_list.append(sentence)
    return train_tfidf(training_list)
    
def train_tfidf_wrm():
    training_list = []
    for file in os.listdir("../data/TaggedDocuments/Labeled"):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            file = json.loads(open(os.path.join("../data/TaggedDocuments/Labeled",filename), "r").read())
            for td in file:
                sentence = ""
                for word in td[0]:
                    sentence+=word + " "
                training_list.append(sentence)
    return train_tfidf(training_list)
    
def score_tfidf_pm(tfidf):
    for file in reversed(os.listdir("../data/profilemanager/TaggedDocuments/Labeled")):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            output = []
            file = json.loads(open(os.path.join("../data/profilemanager/TaggedDocuments/Labeled",filename), "r").read())
            for td in file:
                sentence = ""
                for word in td[0]:
                    sentence+=word + " "
                try:
                    score = get_relevance_score(tfidf, sentence)
                    output.append([score, td[0]])
                except Exception as e:
                    print("Exception during {}: {}".format(td[1][0], str(e)))
            file = open("../data/profilemanager/TaggedDocuments/Classified/output_{}".format(filename), "w")
            file.write(json.dumps(output, sort_keys = True, indent = 4))
            file.close()
            print("Finished scoring {}".format(filename))
            
def score_tfidf_wrm(tfidf):
    for file in os.listdir("../data/TaggedDocuments/Labeled"):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            output = []
            file = json.loads(open(os.path.join("../data/TaggedDocuments/Labeled",filename), "r").read())
            for td in file:
                sentence = ""
                for word in td[0]:
                    sentence+=word + " "
                try:
                    score = get_relevance_score(tfidf, sentence)
                    output.append([score, td[0]])
                except Exception as e:
                    print("Exception during {}: {}".format(td[1][0], str(e)))
            file = open("../data/TaggedDocuments/Classified/output_{}".format(filename), "w")
            file.write(json.dumps(output, sort_keys = True, indent = 4))
            file.close()
            file.close()
            print("Finished scoring {}".format(filename))

def get_TaggedDocuments_pm(pm, instances, iam):
        good = []
        bad = []
        idk = []
        count = 0
        numPerList = 10000
        with open(os.path.join("../data/profilemanager/data", "names.json"), "r") as handle:
            names = json.loads(handle.read())
        with open(os.path.join("../data/profilemanager/data", "cas_from_wiki.json"), "r") as handle:
            cas = json.loads(handle.read())
        templist = [word_tokenize(word) for word in names] + [word_tokenize(word) for word in cas]
        goodlist = []
        for wordlist in templist:
            for word in wordlist:
                goodlist.append(word)
        goodlist = goodlist
        for text, tag in pm.get_docs_by_sentence(instances, iam):
            text = convert_to_corpus(text)
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
                for word in ['call', 'pursuant', 'accord', 'security', 'goodwill', 'registrant', 'amendment', 'transit', 'proxy', 'stockholder', 'disclosure', 'mission', 'share', 'flow', 'amortize', 'pension', 'depreciate', 'statement', 'certify', 'recieviable', 'payable', 'license', 'expense', "jurisdiction", "----", "gaap" ]:
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
                file = open("../data/profilemanager/TaggedDocuments/Labeled/{}_{}_{}.json".format("good_sentences", iam, count//numPerList), "w")
                file.write(json.dumps(good, sort_keys = True, indent = 4))
                file.close()
                file = open("../data/profilemanager/TaggedDocuments/Labeled/{}_{}_{}.json".format("bad_sentences", iam, count//numPerList), "w")
                file.write(json.dumps(bad, sort_keys = True, indent = 4))
                file.close()
                file = open("../data/profilemanager/TaggedDocuments/Labeled/{}_{}_{}.json".format("idk_sentences", iam, count//numPerList), "w")
                file.write(json.dumps(idk, sort_keys = True, indent = 4))
                file.close()
                good = []
                bad = []
                idk = []
                
        file = open("../data/profilemanager/TaggedDocuments/Labeled/{}_{}_{}.json".format("good_sentences", iam, count//numPerList), "w")
        file.write(json.dumps(good, sort_keys = True, indent = 4))
        file.close()
        file = open("../data/profilemanager/TaggedDocuments/Labeled/{}_{}_{}.json".format("bad_sentences", iam, count//numPerList), "w")
        file.write(json.dumps(bad, sort_keys = True, indent = 4))
        file.close()
        file = open("../data/profilemanager/TaggedDocuments/Labeled/{}_{}_{}.json".format("idk_sentences", iam, count//numPerList), "w")
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
                    text = convert_to_corpus(sent_list[i])
                    tag = "{}{:04d}".format(item['id'], i)
                    letters_in_sentence = sum([len(w) for w in text])
                    if letters_in_sentence > 750 or letters_in_sentence < 25:
                        tagged = True
                        bad.append(TaggedDocument(words=text, tags=list({tag, "bad"})))
                    if not tagged:
                        words = 0
                        bad_words = 0
                        for word in text:
                            words+= 1
                            if len(word) < 2 or len(word) > 10:
                                bad_words+= 1
                        if bad_words/words > .9:
                            tagged = True
                            bad.append(TaggedDocument(words=text, tags=list({tag, "bad"})))
                    if not tagged:
                        for word in [ 'skip to main content',  'remember my device', "toggle menu", "user agreement" "privacy statement", "terms of service", "javascript", "footer", "header", "subscribe",  "contact us", "usage has been flagged"]:
                            if not tagged and word in sent_list[i] or len(sent_list[i]) < 3:
                                tagged = True
                                bad.append(TaggedDocument(words=text, tags=list({tag, "bad"})))
                    if not tagged:
                        idk.append(TaggedDocument(words=text, tags=list({tag})))
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
                
def score_docs_pm():
    model = Doc2Vec.load("../data/profilemanager/doc2vec_model")
    i = 0
    for file in os.listdir("../data/profilemanager/TaggedDocuments"):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            output = []
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
            
def score_docs_wrm():
    model = Doc2Vec.load("../data/doc2vec_model")
    i = 0
    for file in os.listdir("../data/TaggedDocuments/Labeled"):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            output = []
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
                docs.append(TaggedDocument(words=[x for x in td[0]], tags=[x for x in td[1]]))
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
#    wrm = WebResourceManager("..")
#    for file in os.listdir("../data/webresourcemanagers"):
#        tmp = WebResourceManager()
#        tmp.load(os.path.join("../data/webresourcemanagers", file))
#        tmp.rel_path = ".."
#        wrm.absorb_file_manager(tmp)
#    get_TaggedDocuments_wrm(wrm)
#    train_model_wrm()
#    score_docs_wrm()
#    pm = ProfileManager("..")
#    get_TaggedDocuments_pm(pm, 6, 0)
#    time.sleep(3000)
#    train_model_pm()
#    score_docs_pm()
    tfidf = train_tfidf_pm()
    score_tfidf_pm(tfidf)
    

if __name__ == "__main__" :
    main()