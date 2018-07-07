# PCATx CORE

A web crawling and artificial intelligence framework for Praedicat, Inc. developed by the 2018 RIPS team at UCLA's Institute for Pure and Applied Mathematics. Our goal utilize Natural Language Processing techniques and Artificial Intelligence to collect automate data collection for the InsurTech company.

![Diagram of PCATx Core Architecture](/img/PCATxCOREArchitecture.jpg)

### Table of Contents
---------------------
* Classifier
* KPM == Keyword Producing Model
* Parser
* Query Formulator

### Classifier
--------------

### Keyword Producing Module (KPM)
---------------------------------

This module is divided into two parts: the Mapper and the Keyword Producing Model (KPM).

Mapper is essentially a wrapper for a dictionary, it associates unique identifiers with a list of aliases for the entity identified. An example would be "00001" -> ["Micron Technology", "MU", "Micron"]. For full documentation on Mapper, go to [docs/Mapper.md](kpm/docs/Mapper.md).

The Keyword Producing Model takes data and finds words highly associated with our entities to build the list of aliases using data2vec and neural networks.

The following modules and scripts are part of the Keyword Producing Model:

* [corpusBuilder.py](kpm/corpusBuilder.py) --- [Documentation](kpm/docs/corpusBuilder.md)
corpusBuilder is a wrapper for a list of lists that is specifically designed to process text documents and get them into a format which is optimal for doc2vec.

* [Mapper.py](Mapper.py) --- [Documentation](kpm/docs/Mapper.md)
Mapper is essentially a wrapper for a dictionary, it associates unique identifiers with a list of aliases for the entity identified. An example would be "00001" -> ["Micron Technology", "MU", "Micron"].

##### /bin

* [ProcessTxtFiles.py](kpm/bin/ProcessTxtFiles.py)
A simple module with functions for processing text files in particular formats we encountered such as the 20 News Groups data set.


### Parser
----------
This is a parser that extracts visible and relevant content from webpages.
It can 1) save original html pages and pdf contents
       2) write new files with relevant html/pdf contents in a directory

# Documentation

|Function | Input        | Processing           | Output  |
|-----   | ------------- |:-------------:| -----:|
|parser(linkList)    | a list of URLs      | create text files | None |
|tag_visible(element)    |  a string of webpage content   | determine if the content in a tag is visible and relevant | True/False|
|text_from_html(body)    |  a string of webpage content  | extract relevant content |a string of visible and relevant text|
|sentence_filter(sentence_list)| a list of sentences | remove non-sentences | a list of sentences after removal|


### Query Formulator
------------------------------------
