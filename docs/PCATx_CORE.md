**Self-Supervised Classifier**
----------------------

## Table of contents
* Introduction
* Documentation

## Introduction

**PCATx_CORE** drives the frameworks described in Milestones One and Two, providing driver functions for supervised and unsupervised runs of the architecture.

## Documentation

##### basic_relevance_filter(document)

Basic relevance filter on the basis of characters in sentence. Filters out sentences with fewer than 50 characters or more than 750 characters.

Parameters
* document (list of strings) : a list of sentences you would like to filter

Returns
* None

##### generate_HTML_output(wrm, table, sub_list, dbresources, name)

Generates an HTML Master Document

Parameters
* wrm (WebResourceManager) : the WebResourceManager tracking the web resources generated for the Master Document
* table (beautifulsoup.table) : the Wikipedia infobox table in HTML
* sub_list (list of strings) : list of subsidiaries
* dbresources (list of tuples (string (text), string (URL))) : a list of resources for the company in the company's profile in Profile Manager
* name (string) : name of the company the Master Document is about (for the title of the doc)

Returns
* None

##### PCATx_CORE_supervised(recursive=True)

Runs the Web Crawling Architecture, PCATx CORE, in a supervised fashion

Asks for a company name as input which it sends to Wikipedia. The dialog then asks if Wikipedia match (if one is found) is the company you are looking for and looks for close matches in the ProfileManager to retrieve relevant company info. From there, the Web Crawler retrieves relevant web pages and generate_HTML_output produces a Master Document, Web Resource Managers for each company are saved.


Parameters
* recursive (bool) : whether or not you'd like to call PCATx_CORE_unsupervised on the list of subsidiaries found (default = True)

Returns
* None

##### PCATx_CORE_unsupervised(list_of_companies)

Runs the Web Crawling Architecture, PCATx CORE, in an unsupervised fashion

The Web Crawler retrieves relevant web pages and generate_HTML_output produces a Master Document for each company in the list, adding subsidiaries found to the queue. Web Resource Managers for each company are saved. The queue is saved as JSON list at "data/PCATx_CORE_unsupervised_save_list.json" every 100 companies and when the function throws an exception

Parameters
* list_of_companies (list of strings) : the list of companies you would like to produce Master Documents for

Returns
* None
