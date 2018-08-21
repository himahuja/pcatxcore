**Self-Supervised Classifier**
----------------------

## Table of contents
* Introduction
* Documentation

## Introduction

Self-Supervised Classifier is a set of functions which together comprise a model for classifying sentences as relevant or not. The approach was inspired by [Banko et al.'s 2007 "Open Information Extraction from the Web"](https://www.aaai.org/Papers/IJCAI/2007/IJCAI07-429.pdf) which used a self-supervised learner to perform open information extraction. We are taking much the same approach to relevancy classification by having the learner tag certain sentences as relevant or irrelevant based on keyword input and then Doc2Vec is trained on these tagged sentences to learn more complex features.

## Documentation

##### convert_to_corpus(doc)

Sets all of the text to lower case, removes all non-alphanumeric characters besides apostrophe (') and hyphen (-) with a Regular Expression. All words are lemmatized and then stemmed.

Parameters
* doc (string or list of strings) : a sentence in either string for or list of words form

Returns
* list of strings : the sentence after the Natural Language Processing techniques have been applied

##### get_TaggedDocuments_pm(pm, instances, iam)

Produces TaggedDocuments and labels them appropriately from the documents in the Profile Manager instance and saves them in "../data/profilemanager/TaggedDocuments/Labeled/". Multithreading safe using instances/iam

Parameters
* pm (ProfileManager) : a ProfileManager with the documents you would like to Tag
* instances (int) : the number of instances you'd like to run in parallel
* iam (int) : the current instance's assignment [0-*instances*) (default = 0)

Returns
* None

##### get_TaggedDocuments_wrm(manager)

Produces TaggedDocuments and labels them appropriately from the documents in the Web Resource Manager instance and saves them in "../data/TaggedDocuments/Labeled/". Multithreading safe using instances/iam

Parameters
* manager (WebResourceManager) : a ProfileManager with the documents you would like to Tag

Returns
* None

##### get_tfidf_score(tfidf, document)

Returns the TF-IDF value of the document using the tfidf instance

Parameters
* tfidf (sklearn.feature_extraction.text.TfidfVectorizer) : a TtfidfVectorizer with 'english' stop words and fitted to the corpus
* document (string) : the document to score

Returns
* float : the TF-IDF score of the document

##### score_docs_pm()

Scores the TaggedDocuments in "../data/profilemanager/TaggedDocuments/Labeled" using Profile Manager Doc2Vec model and saves them in "../data/profilemanager/TaggedDocuments/Classified/".

Returns
* None

##### score_docs_wrm()

Scores the TaggedDocuments in "../data/TaggedDocuments/Labeled" using Web Resource Manager Doc2Vec model and saves them in "../data/TaggedDocuments/Classified/".

Returns
* None

##### score_tfidf_pm(tfidf)

Scores the documents in the Profile Manager instance using TF-IDF and saves them in "../data/profilemanager/TaggedDocuments/Classified/". Multithreading safe using instances/iam.

Parameters
* tfidf (sklearn.feature_extraction.text.TfidfVectorizer) : a TtfidfVectorizer with 'english' stop words and fitted to the Profile Manager corpus
* instances (int) : the number of instances you'd like to run in parallel
* iam (int) : the current instance's assignment [0-*instances*) (default = 0)

Returns
* None

##### score_tfidf_wrm(tfidf)

Scores the documents in the Profile Manager instance using TF-IDF and saves them in "../data/TaggedDocuments/Classified/"

Parameters
* tfidf (sklearn.feature_extraction.text.TfidfVectorizer) : a TtfidfVectorizer with 'english' stop words and fitted to the Web Resource Manager corpus

Returns
* None

##### train_model_pm()

Trains a Profile Manager Doc2Vec model using the TaggedDocuments in "../data/profilemanager/TaggedDocuments/Labeled/" and saves the model at "../data/profilemanager/doc2vec_model"

Returns
* None

##### train_model_wrm()

Trains a Web Resource Manager Doc2Vec model using the TaggedDocuments in "../data/TaggedDocuments/Labeled" and saves the model at "../data/doc2vec_model"

Returns
* None

##### train_tfidf(corpus)

Instantiates and trains a TF-IDF Vectorizer using the English stop words

Parameters
* corpus (list of strings) : the corpus you would like to perform TF-IDF on

Returns
* sklearn.feature_extraction.text.TfidfVectorizer : a TtfidfVectorizer with 'english' stop words and fitted to the data.

##### train_tfidf_pm()

Returns a TF-IDF instance trained on the Profile Manager instance

Returns
* sklearn.feature_extraction.text.TfidfVectorizer : a TtfidfVectorizer with 'english' stop words and fitted to the Profile Manager corpus

##### train_tfidf_wrm()

Returns a TF-IDF instance trained on the Profile Manager instance

Returns
* sklearn.feature_extraction.text.TfidfVectorizer : a TtfidfVectorizer with 'english' stop words and fitted to the Web Resource Manager corpus
