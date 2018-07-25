# Knowledge Management

## Table of Contents

* Introduction
  * Milestone One
  * Milestone Two
* Components
  * WebResourceManager
  * ProfileManager
  * Knowledge Graph

### Introduction
----------------

Knowledge Management is a section of PCATx CORE which is currently being developed as part of PCATx CORE, a web crawling and artificial intelligence framework for Praedicat, Inc. by the 2018 RIPS team at UCLA's Institute for Pure and Applied Mathematics. Our goal is to utilize Natural Language Processing techniques and Artificial Intelligence to automate data collection for the InsurTech company. Knowledge Management specifically deals with management, representation, and classification of data.

Analysts at Praedicat, Inc., need to manually associate each company with a set of business activities. Using this information, analysts attempt to find evidence linking businesses with potentially dangerous practices, such as the use of hazardous chemicals. With a plethora of companies and business activities, manual search is a tedious process. Further, the analysis is generally performed on unstructured, non-uniform, and sporadic Internet sites which makes it difficult to algorithmically search for the information needed and complex to determine the semantic meaning of the documents even when they are found. Our work attempts to tackle these problems by building a web crawler which procures information and comparing the statements found in the documents to a credible knowledge base. Based on computational fact checking, we are hoping this approach will lead to better classification of unstructured text information on the Internet.

<div align="center">
  <img alt="Diagram of PCATx Core Architecture" src="/img/PCATxCOREArchitecture.jpg">
</div>

#### Milestone One

<div align="center">
  <img alt="Diagram of Milestone 1 of the PCATx Core Architecture" src="/img/Milestone1.jpg">
</div>

Milestone One is the web crawling part of our work. It consists of designing and implementing an intelligent web crawler that is able to find relevant information for Praedicat, Inc.'s analysts. Currently all of our work is focused on Milestone One.

#### Milestone Two

<div align="center">
  <img alt="Diagram of Milestone 2 of the PCATx Core Architecture" src="/img/Milestone2.jpg">
</div>

Milestone 2 is much more Natural Language Processing focused, we will be trying to automate refining, structuring, and interpreting the data as much as possible to make the job of Praedicat analysts as easy as possible. Ideally, we should be providing the analysts with a summary document for each company including the company's profile, the system's belief's about the company's associations with potential litigation causing agents, and sources. The simpler it is for the analyst to verify the better and although we would like to avoid all errors, we especially want to minimize Type II errors ("false negatives").

## Components

This module is divided into two parts: Data Management and Classification.

### Data Management

<div align="center">
  <img alt="Diagram of PCATx Core's Data Management" src="/img/DataManagement.jpg">
</div>

##### WebResourceManager

* [WebResourceManager.py](WebResourceManager.py) --- [Documentation](docs/WebResourceManager.md)\
WebResourceManager is a class for helping manage a database of web resources. WebResourceManager creates a UUID (Universally Unique Identifier) for the web resource, saves the information in a JSON (labeled < UUID >.json), and builds maintain a dictionary from  URL to UUID. Using this uniform data storage system and a simple API, WebResourceManager makes storing and querying the contents and source files (such as HTML and PDF) of web resources much simpler.

##### ProfileManager

* [ProfileManager.py](ProfileManager.py) --- [Documentation](docs/ProfileManager.md)\
ProfileManager is a class for helping manage a database of business profiles. It uses the SEC's (United States Securities and Exchange Commission) CIK codes (Central Index Key) to act as identifiers and allows the user to compile a variety of information on corporate entities in an easy to use and query format. Assisting the accessibility of information, ProfileManager supports using a series of mappings from CIK codes to names and back, names to aliases, and mappings from industry code standards and descriptions of them. The hope to provide for a flexible data solution for complex business oriented applications.

### Data Classification

<div align="center">
  <img alt="Diagram of PCATx Core's Classifier" src="/img/Classifier.jpg">
</div>

##### Knowledge Graph

* Knowledge Graph --- [Documentation](docs/KnowledgeGraph.md)\
Currently in development. We are hoping to use computational fact-checking and knowledge graph concepts to implement a classification and credibility checking module. To see the concepts and papers we are exploring, feel free to check out the "Computational Fact-Checking" section of my [AIReading Github](https://github.com/alexandermichels/AIReading#computational-fact-checking).
