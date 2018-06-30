**Mapper**
----------

Mapper is essentially a wrapper for a dictionary, it associates unique identifiers with a list of aliases for the entity identified. An example would be "00001" -> ["Micron Technology", "MU", "Micron"].

##### `__init__(file=None)`

* **file** is the name of the JSON file with the current information you would like to load into the Mapper object

Just a constructor

##### `__contains__(key)`

* **key** is the unique identifier which is associated to a value or list of values

Shortcut for accessing the dictionary shortcut to accessing "in" and "__contains__" for the dict in it

> mapper.`__contains__`("0000001") -> True
> "0000001" in mapper -> True

##### `__delitem__(key)`

* **key** is the unique identifier which is associated to a value or list of values

> del mapper["0000001"]

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
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;],\
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

##### add(key, value)

* **key** is the key you wish to associate the value within
* **value** is the value to be added to the list of aliases associated with the key

Appends the value to the list of value associated with the key

##### clear()

Clears the values from the contained dictionary.

##### items()

Acts a shortcut to items for the dict contained. Returns a list of tuples with (key, value) pairs.

> dict_items([('0000001', ['Micron Technology, Inc.', 'Micron', 'MU', 'Micron Technology', 'Micron Tech']), ('0000002', ['Olin Corporation', 'Olin', 'OLN', 'Olin Corp']), ('0000003', ['Intel Corporation', 'Intel', 'INTC', 'Intel Corp'])])

##### keys()

Acts a shortcut to the *keys()* method. Returns a list of keys.

> dict_keys(['0000001', '0000002', '0000003'])

##### pop(key)

* **key** the identifier which you wish to remove from the dictionary

Acts a shortcut to the *pop()* method, and catches **KeyError** by return empty list. Deletes the **key** and returns it's associated values.

##### update(other_key_value)

* **other_key_value** is either another dictionary object or an iterable of key/value pairs (as tuples or other iterables of length two)

Update the dictionary with the key/value pairs from other, overwriting existing keys.

##### values()

Acts a shortcut to the inside dict's *values()* method

> dict_values([['Micron Technology, Inc.', 'Micron', 'MU', 'Micron Technology', 'Micron Tech'], ['Olin Corporation', 'Olin', 'OLN', 'Olin Corp'], ['Intel Corporation', 'Intel', 'INTC', 'Intel Corp']])
