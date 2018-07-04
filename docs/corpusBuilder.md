**corpusBuilder**
----------------

corpusBuilder is a wrapper for a list of lists that is specifically designed to process text documents and get them into a format which is optimal for doc2vec.

##### `__init__(dirname=None)`

* **dirname** is the name of the directory holding the text files you wish to process. The reason you may want to keep this unspecified is to initialize the corpusBuilder in another way such as with the **load()** function.

This function decodes using the "UTF-8" codec, ignoring errors, uses regular expressions to remove special characters and numbers, and filters out certain "stop words" by calling **filter_dict()**.

##### `__getitem__(key)`

* **key** is the index of the item you would like to access in the list inside of corpusBuilder

Allows you to treat a corpusBuilder object as a list with the **[]** operator

##### `__iter__()`

Successively yields elements of the contained list.

##### `__len__()`

Returns the number of elements (lists) of the contained list.

##### `__repr__()` `__str__()`

Returns a string representation of the object.

##### filter_dict()

Uses a set of stop words and removes the specified words from the list of lists.

TODO: Generate a better list and add more functionality here. Use doc2vec to generate?

##### load(file_name)

* **file_name** is the name of a JSON file which contains a corpusBuilder object

Attempts to load the corpusBuilder's list from the JSON

##### save(file_name)

* **file_name** is the name of a JSON file which you wish to write the corpusBuilder object to

Attempts to write the corpusBuilder object's list to the specified object

##### to_TaggedDocument()

Returns a list of **TaggedDocument** objects using the contained documents stored in the list of lists. Each list becomes a **TaggedDocument**. This format is necessary for doc2vec.

TODO: look into the meaning/importance of the **tags** parameter of the **TaggedDocument** object
