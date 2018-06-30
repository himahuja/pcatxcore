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

##### `__init__(file=None)`

* **file** is the name of the JSON file with the current information you would like to load into the Mapper object

Just a constructor

##### `__contains__(key)`

* **key** is the unique identifier which is associated to a value or list of values

Shortcut for accessing the dictionary shortcut to accessing "in" and "__contains__" for the dict in it

> mapper.__contains("0000001") -> True
> "0000001" in mapper -> True

##### `__delitem__(key)`

* **key** is the unique identifier which is associated to a value or list of values

##### `__getitem__(key)`, get(key), id_to_alias(key)

* **key** is the unique identifier which will be used as a key to return the list of aliases (in string) associated with the key

Allows you to treat the object (Mapper) like the dictionary inside of it. Catches KeyErrors by return any empty list

> mapper["0000001"] -> ['Micron Technology, Inc.', 'Micron', 'MU', 'Micron Technology', 'Micron Tech']
> mapper.get["0000001"] -> ['Micron Technology, Inc.', 'Micron', 'MU', 'Micron Technology', 'Micron Tech']
> mapper.id_to_alias["0000001"] -> ['Micron Technology, Inc.', 'Micron', 'MU', 'Micron Technology', 'Micron Tech']

##### `__len__`

Returns the number of keys in the dictionary in the Mapper object

> len(mapper) -> 3

##### `__repr__` , `__str__`

Prints the dictionary in a pretty JSON format.

> {\
&nbsp;&nbsp;&nbsp;&nbsp;"0000001": [\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"Micron Technology, Inc.",\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"Micron",\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"MU",\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"Micron Technology",\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"Micron Tech"\
&nbsp;&nbsp;&nbsp;&nbsp;],\
&nbsp;&nbsp;&nbsp;&nbsp;"0000002": [\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"Olin Corporation",\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"Olin",\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"OLN",\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"Olin Corp"\
&nbsp;&nbsp;&nbsp;&nbsp;],\
&nbsp;&nbsp;&nbsp;&nbsp;"0000003": [\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"Intel Corporation",\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"Intel",\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"INTC",\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"Intel Corp"\
&nbsp;&nbsp;&nbsp;&nbsp;]\
}

##### `__setitem__(key, value)`

* **key** is the key which is being changed
* **value** is the value which is being changed

Acts as a shortcut to access the dict within

> mapper["0000001"] = ['Micron Technology, Inc.', 'Micron', 'MU', 'Micron Technology', 'Micron Tech']


### Parser
----------

### Query Formulator
------------------------------------
