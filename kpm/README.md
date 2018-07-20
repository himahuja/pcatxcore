# Keyword Producing Module (KPM)
-------------------------------

The Keyword Producing Module (KPM) is a section of PCATx CORE which is currently being developed as part of PCATx CORE, a web crawling and artificial intelligence framework for Praedicat, Inc. by the 2018 RIPS team at UCLA's Institute for Pure and Applied Mathematics. Our goal is to utilize Natural Language Processing techniques and Artificial Intelligence to automate data collection for the InsurTech company.

Analysts at Praedicat, Inc., need to manually associate each company with a set of business activities. Using this information, analysts attempt to find evidence linking businesses with potentially dangerous practices, such as the use of hazardous chemicals. With a plethora of companies and business activities, manual search is a tedious process. Further, the analysis is generally performed on unstructured, non-uniform, and sporadic internet sites which makes it difficult to algorithmically search for the information needed and complex to determine the semantic meaning of the documents even when they are found. Our work attempts to tackle these problems by building a web crawler which procures information and comparing the statements found in the documents to a credible knowledge base. Based on computational fact checking, we are hoping this approach will lead to better classification of unstructured text information on the internet.

![Diagram of PCATx Core Architecture](/img/PCATxCOREArchitecture.jpg)

This module is divided into two parts: the Mapper and the Keyword Producing Model (KPM).

Mapper is essentially a wrapper for a dictionary, it associates unique identifiers with a list of aliases for the entity identified. An example would be "00001" -> ["Micron Technology", "MU", "Micron"]. For full documentation on Mapper, go to [docs/Mapper.md](docs/Mapper.md).

The Keyword Producing Model takes data and finds words highly associated with our entities to build the list of aliases using data2vec and neural networks.

The following modules and scripts are part of the Keyword Producing Model:

* [corpusBuilder.py](corpusBuilder.py) --- [Documentation](docs/corpusBuilder.md)
**Note: Currently deprecated. The functionality this previously served is now served by [WebResourceManager.py](../knowledge_management/WebResourceManager.py)**
corpusBuilder is a wrapper for a list of lists that is specifically designed to process text documents and get them into a format which is optimal for doc2vec.

* [Mapper.py](Mapper.py) --- [Documentation](docs/Mapper.md)
**Note: Currently deprecated. The functionality this previously served is now served by [ProfileManager.py](../knowledge_management/ProfileManager.py)**
Mapper is essentially a wrapper for a dictionary, it associates unique identifiers with a list of aliases for the entity identified. An example would be "00001" -> ["Micron Technology", "MU", "Micron"].

##### /bin

* [ProcessTxtFiles.py](bin/ProcessTxtFiles.py)
A simple module with functions for processing text files in particular formats we encountered such as the 20 News Groups data set.
