# PCATx CORE

A web crawling and artificial intelligence framework for Praedicat, Inc. developed by the 2018 RIPS team at UCLA's Institute for Pure and Applied Mathematics. Our goal utlize Natural Language Processing techniques and Artificial Intelligence to collect automate data collection for the InsurTech company.

### Table of Contents
---------------------
* Classifier
* KPM == Keyword Producing Model
* Parser
* Query Formulator

### Classifier
--------------

### Mapper and Keyword Producing Model (KPM)
--------------------------------------------

This module is divided into two parts: the Mapper and the Keyword Producing Model (KPM). The Mapper is essentially a wrapper for a dictionary, it associates unique identifiers with a list of aliases for the entity identified. An example would be "00001" -> ["Micron Technology", "MU", "Micron"]. The Keyword Producing Model takes input from other 

#### **Mapper**

##### __init__(file=None)

* **file** is the name of the JSON file with the current information you would like to load into the Mapper object

Just a constructor

##### __getitem__(id), get(id), id_to_alias(id)

* **id** is the unique identifier which will be used as a key to return the list of aliases (in string) associated with the key

Allows you to treat the object (Mapper) like the dictionary inside of it

> mapper["0000001"] -> ['Micron Technology, Inc.', 'Micron', 'MU', 'Micron Technology', 'Micron Tech']
> mapper.get["0000001"] -> ['Micron Technology, Inc.', 'Micron', 'MU', 'Micron Technology', 'Micron Tech']
> mapper.id_to_alias["0000001"] -> ['Micron Technology, Inc.', 'Micron', 'MU', 'Micron Technology', 'Micron Tech']

##### __repr__, __str__

Prints the dictionary in a pretty JSON format.

> {\
    "0000001": [\
        "Micron Technology, Inc.",\
        "Micron",\
        "MU",\
        "Micron Technology",\
        "Micron Tech"\
    ],\
    "0000002": [\
        "Olin Corporation",\
        "Olin",\
        "OLN",\
        "Olin Corp"\
    ],\
    "0000003": [\
        "Intel Corporation",\
        "Intel",\
        "INTC",\
        "Intel Corp"\
    ]\
}\

### Parser
----------

### Query Formulator
------------------------------------


