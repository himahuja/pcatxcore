# PCATx CORE

### Table of Contents
---------------------
* Introduction
  * Milestone One
  * Milestone Two
  * Milestone Three
* Milestone One
  * Query Formulator
  * Web Crawler
  * Parser
  * WebResourceManager
* Milestone Two
  * Classifier
  * ProfileManager
  * PCATx_CORE

### Introduction
----------------

PCATx CORE is currently being developed as a web crawling and artificial intelligence framework for Praedicat, Inc. by the 2018 RIPS team at UCLA's Institute for Pure and Applied Mathematics. Our goal is to utilize Natural Language Processing techniques and Artificial Intelligence to automate data collection for the InsurTech company.

Analysts at Praedicat, Inc., need to manually associate each company with a set of business activities. Using this information, analysts attempt to find evidence linking businesses with potentially dangerous practices, such as the use of hazardous chemicals. With a plethora of companies and business activities, manual search is a tedious process. Further, the analysis is generally performed on unstructured, non-uniform, and sporadic Internet sites which makes it difficult to algorithmically search for the information needed and complex to determine the semantic meaning of the documents even when they are found. Our work attempts to tackle these problems by building a web crawler which procures information and comparing the statements found in the documents to a credible knowledge base. Based on computational fact checking, we are hoping this approach will lead to better classification of unstructured text information on the Internet.

For the ability to conform to the [Robots Exclusion Standard](https://en.wikipedia.org/wiki/Robots_exclusion_standard), we have also developed a simple set of functions in [Robots-Exclusion-Standard-Handler](https://github.com/alexandermichels/Robots-Exclusion-Standard-Handler).

To learn more about the concepts we explored while developing this project including Computational Fact-Checking, Information Extraction, and Knowledge Graphs, all of the papers and resources the team consulted over the course of their work can be found here: [RIPS Readings](https://github.com/alexandermichels/RIPSReadings)

<div align="center">
  <img alt="Diagram of PCATx Core Architecture" src="/img/Milestones1and2.png">
</div>

#### Milestone One

<div align="center">
  <img alt="Diagram of Milestone 1 of the PCATx Core Architecture" src="/img/Milestone1.png">
</div>

Milestone One is the web crawling part of our work. It consists of designing and implementing an intelligent web crawler that is able to find relevant information for Praedicat, Inc.'s analysts. Currently all of our work is focused on Milestone One.

#### Milestone Two

<div align="center">
  <img alt="Diagram of Milestone 2 of the PCATx Core Architecture" src="/img/Milestone2.png">
</div>

Milestone 2 is much more Natural Language Processing focused, we will be trying to automate refining, structuring, and interpreting the data as much as possible to make the job of Praedicat analysts as easy as possible. Ideally, we should be providing the analysts with a summary document for each company including the company's profile, the system's belief's about the company's associations with potential litigation causing agents, and sources. The simpler it is for the analyst to verify the better and although we would like to avoid all errors, we especially want to minimize Type II errors ("false negatives").

### Milestone One
-----------------

##### Query Formulator

<div align="center">
  <img alt="Diagram of PCATx Core's Query Formulator" src="/img/QueryFormulator.png">
</div>

##### Web Crawler

<div align="center">
  <img alt="Diagram of PCATx Core's Web Crawler" src="/img/WebCrawler.png">
</div>

* [webcrawlAll.py](/webcrawlAll.py) --- [Documentation](docs/webcrawllAll.md)\
webcrawlAll is a set of modules to crawl various credible websites (TRI, EPA and SEC). Each of these modules is accessible from the module: `crawlerWrapper` which specifies various *engines*.
  * `google`: calls `search_google`.
  * `sec10k`: [*Deprecated*] constructs the url with `urlmaker_sec` and calls the `search_sec10k` for that CIK code.
  * `sec10kall`: engine is related to `sec10k`, but it runs for a CIK dict rather than a single CIK.
  * `secsic10k`: gets the 10-Ks related to that company for the SEC group.
  * `generalSEC`: make a general query to the SEC website, uses `urlmaker_sec`.
  * `sitespecific`:  Uses *httrack* to download index and PDFs from the input website.
  * `google-subs`: Pulls the subsidaries out of Google
  * `everything-all`: Pulls out the 10Ks, 8Ks, and E-21s for a CIK dictionary

[Site_Crawler_Parser_All.py](Site_Crawler_Parser_All.py) --- [Documentation](docs/Site_Crawler_Parser_All.md)\

* A crawler and parser for **Wikipedia pages** that can parse information in a Wikipedia infobox into a Python Dictionary and the article text as a string.
* A crawler and parser for **all-level subsidiaries returned by Google** that can parse subsidiary names on a search result page into a Python Dictionary.
* A crawler and parser for **TRI facility reports** that can parse a facility information table into a Python Dictionary and a chemical usage report into a comma-separated values (CSV) file.
* A crawler and parser for **EWG search results** that can parse name of products by a company and ingredients in a product into a Python Dictionary.
* A crawler and parser for **NPIRS search results** that can parse names of manufacturers that use a certain hazard into a Python Dictionary.

##### Parser

<div align="center">
  <img alt="Diagram of PCATx Core's Parser" src="/img/Parser.png">
</div>

This is a parser that extracts visible and relevant content from webpages.
It can
* save original html pages and pdf contents
* write text files with the contents in a directory

###### Documentation

|Function | Input        | Processing           | Output  |
|-----   | ------------- |:-------------:| -----:|
|parser(linkList)    | a list of URLs      | create text files | None |
|tag_visible(element)    |  a string of webpage content   | determine if the content in a tag is visible and relevant | True/False|
|text_from_html(body)    |  a string of webpage content  | extract relevant content |a string of visible and relevant text|
|sentence_filter(sentence_list)| a list of sentences | remove non-sentences | a list of sentences after removal|

##### WebResourceManager

<div align="center">
  <img alt="Diagram of PCATx Core's Classifier" src="/img/WebResourceManager.png">
</div>

* [WebResourceManager.py](WebResourceManager.py) --- [Documentation](knowledge_management/docs/WebResourceManager.md)\
WebResourceManager is a class for helping manage a database of web resources. WebResourceManager creates a UUID (Universally Unique Identifier) for the web resource, saves the information in a JSON (labeled < UUID >.json), and builds maintain a dictionary from  URL to UUID. Using this uniform data storage system and a simple API, WebResourceManager makes storing and querying the contents and source files (such as HTML and PDF) of web resources much simpler.

### Milestone Two
-----------------

### Classifier

<div align="center">
  <img alt="Diagram of PCATx Core's Classifier" src="/img/Classifier.png">
</div>

* [Self-Supervised Classifier](knowledge_management/SelfSupervisedClassifier.py) ---
[Documentation](knowledge_management/docs/SelfSupervisedClassifier.md)\
A model for classifying sentences as relevant or not. The approach was inspired by [Banko et al.'s 2007 "Open Information Extraction from the Web"](https://www.aaai.org/Papers/IJCAI/2007/IJCAI07-429.pdf) which used a self-supervised learner to perform open information extraction. We are taking much the same approach to relevancy classification by having the learner tag certain sentences as relevant or irrelevant based on keyword input and then Doc2Vec is trained on these tagged sentences to learn more complex features.

<div align="center">
  <img alt="Diagram of PCATx Core's Classifier" src="/img/ProfileManager.png">
</div>

##### ProfileManager

* [ProfileManager.py](ProfileManager.py) --- [Documentation](knowledge_management/docs/ProfileManager.md)\
ProfileManager is a class designed for the aggregation of information related to corporate entities to support building business profiles. It uses the United States Securities and Exchange Commission (SEC) Central Index Key (CIK) to act as universally unique identifiers (UUIDs) and allows the user to compile a variety of information on corporate entities in an easy to use and query format because each profile is a dictionary. Assisting the accessibility of information, **Profile Manager** includes a series of mappings from CIK codes to names and back, names to aliases, and mappings from industry codes (namely The North American Industry Classification System (NAICS) and Standard Industrial Classification (SIC) codes) and descriptions of them. The hope to provide for a flexible data solution for complex business oriented applications.

##### PCATx_CORE

* [PCATx_CORE.py](PCATx_CORE.py) --- Documentation in Progress
