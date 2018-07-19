# PCATx CORE

A web crawling and artificial intelligence framework for Praedicat, Inc. developed by the 2018 RIPS team at UCLA's Institute for Pure and Applied Mathematics. Our goal utilize Natural Language Processing techniques and Artificial Intelligence to collect automate data collection for the InsurTech company.

![Diagram of PCATx Core Architecture](/img/PCATxCOREArchitecture.jpg)

### Table of Contents
---------------------
* Classifier
* Parser
* Profile Manager
* Query Formulator
* Web Crawler
* Web Resource Manager

### Classifier
--------------

Currently in development. We are hoping to use computational fact-checking and knowledge graph concepts to implement a classification and credibility checking module. To see the concepts and papers we are exploring, feel free to check out the "Computational Fact-Checking" section of my [AIReading Github](https://github.com/alexandermichels/AIReading#computational-fact-checking).


### Parser
----------
This is a parser that extracts visible and relevant content from webpages.
It can
* save original html pages and pdf contents
* write new files with relevant html/pdf contents in a directory

##### Documentation

|Function | Input        | Processing           | Output  |
|-----   | ------------- |:-------------:| -----:|
|parser(linkList)    | a list of URLs      | create text files | None |
|tag_visible(element)    |  a string of webpage content   | determine if the content in a tag is visible and relevant | True/False|
|text_from_html(body)    |  a string of webpage content  | extract relevant content |a string of visible and relevant text|
|sentence_filter(sentence_list)| a list of sentences | remove non-sentences | a list of sentences after removal|


### Profile Manager
-------------------


### Query Formulator
--------------------

### Web Crawler
---------------

### Web Resource Manager
-------------------------------

* [WebResourceManager.py](knowledge_management/WebResourceManager.py) --- [Documentation](knowledge_management/docs/WebResourceManager.md)
WebResourceManager is a class for helping manage a database of web resources. WebResourceManager creates a UUID (Universally Unique Identifier) for the web resource, saves the information in a JSON (labeled < UUID >.json), and builds maintain a dictionary from  URL to UUID. Using this uniform data storage system and a simple API, WebResourceManager makes storing and querying the contents and source files (such as HTML and PDF) of web resources much simpler.
