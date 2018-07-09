**FileManager**
----------------

FileManager is a class for helping manage a database of web resources. FileManager creates a UUID (Universally Unique Identifier) for the web resource, saves the information in a JSON (labeled < UUID >.json), and builds maintains two dictionaries: UUID to URL and URL to UUID. Using this uniform data storage system and a simple API, FileManager makes storing and querying the contents and source files (such as HTML and PDF) of web resources much simpler.

##### `__init__(rel_path=None)`

* **rel_path** is the relative path from the current working directory to the directory where the files you'd like to work with are.

Just instantiates the object.

##### `__iter__()`

Returns an iterator for the JSONs holding the web resource information.

##### `__getitem__(key)` and get(key)

* **key** is the UUID of the web resource content you would like to access.

##### `__len__()`

Returns the number of web resources currently being tracked by the FileManager object.

##### `__repr__()` and `__str__()`

Returns a string representation of the FileManager object using JSON.

##### load(file_name=None)

* **file_name** is the name of the file you wish to load a FileManager from.

Reads in the FileManager object from a file. The default is "data/filemanager.json" and if rel_path was specified it will be "rel_path/data/filemanager.json"

##### read_in_docs(iterator_of_docs)

* **iterator_of_docs** is an iterator of documents which are just dictionaries with a **text**, **query**, **url**, and either **html** or **pdf** attributes.

For each document, the method generates a UUID, adds itself to both dictionaries, writes the appropriate source file (< UUID >.html or < UUID >.pdf), and writes a content JSON with the **id**, **query**, **text**, and **url** fields.

##### string_to_uuid(string)

* **string** is a string, in practice it is generally the URL of the web resource

Returns the UUID for the web resource.

##### save(file_name=None)

* **file_name** is the name of the file you wish to save the FileManager to.

Writes the FileManager object to the **file_name** if specified. Otherwise, it writes to "data/filemanager.json" or "rel_path/data/filemanager.json" if rel_path was specified.

##### url_to_uuid(url)

* **url** is the URL of the web resource

Returns the UUID of the web resource with the specified URL.

##### uuid_to_url(key)

* **key** is the UUID of the web resource.

Returns the URL of the web resource specified with the UUID.
