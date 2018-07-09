# Keyword Producing Module (KPM)
-------------------------------

The Keyword Producing Module (KPM) is currently being developed as part of PCATx CORE, a web crawling and artificial intelligence framework for Praedicat, Inc. developed by the 2018 RIPS team at UCLA's Institute for Pure and Applied Mathematics. Our goal utilize Natural Language Processing techniques and Artificial Intelligence to collect automate data collection for the InsurTech company.

![Diagram of PCATx Core Architecture](/img/PCATxCOREArchitecture.jpg)

This module is divided into two parts: the Mapper and the Keyword Producing Model (KPM).

Mapper is essentially a wrapper for a dictionary, it associates unique identifiers with a list of aliases for the entity identified. An example would be "00001" -> ["Micron Technology", "MU", "Micron"]. For full documentation on Mapper, go to [docs/Mapper.md](docs/Mapper.md).

The Keyword Producing Model takes data and finds words highly associated with our entities to build the list of aliases using data2vec and neural networks.

The following modules and scripts are part of the Keyword Producing Model:

* [corpusBuilder.py](corpusBuilder.py) --- [Documentation](docs/corpusBuilder.md)
corpusBuilder is a wrapper for a list of lists that is specifically designed to process text documents and get them into a format which is optimal for doc2vec.

* [FileManager.py](../FileManager.py) --- [Documentation](docs/FileManager.md)
FileManager is a class for helping manage a database of web resources. FileManager creates a UUID (Universally Unique Identifier) for the web resource, saves the information in a JSON (labeled < UUID >.json), and builds maintains two dictionaries: UUID to URL and URL to UUID. Using this uniform data storage system and a simple API, FileManager makes storing and querying the contents and source files (such as HTML and PDF) of web resources much simpler.

* [Mapper.py](Mapper.py) --- [Documentation](docs/Mapper.md)
Mapper is essentially a wrapper for a dictionary, it associates unique identifiers with a list of aliases for the entity identified. An example would be "00001" -> ["Micron Technology", "MU", "Micron"].

##### /bin

* [ProcessTxtFiles.py](bin/ProcessTxtFiles.py)
A simple module with functions for processing text files in particular formats we encountered such as the 20 News Groups data set.
