
# PieDB

**Simple, Fast, and Lightweight Data Storage**

Tired of setting up complex databases for small projects? 
PieDB gives you a hassle-free way to store and manage structured data using just a JSON file. It is here to keep things simple. Designed for speed and efficiency, it lets you store and retrieve structured data effortlessly—no setup, no hassle.

- 🎒🔧 Schema Enforcement: Ensures data consistency and integrity across your collections.

- 🌟✨ CLI Management: Provides an interactive command-line interface for seamless database operations.

- 🔧🧩 Modular Utilities: Offers utility functions for ID generation, schema normalization, and data encoding.

- 🚀⚡ Fast CRUD & Querying: Supports efficient create, read, update, delete, and filter operations.

- 🛡️🔒 Robust Error Handling: Custom exceptions to maintain data integrity and clear failure states.

- 💾🧩 Backup & Restore: Simplifies data backup and restoration processes for reliable data management.

Whether you're building a small app, prototyping, or need a lightweight alternative to traditional databases, PieDB keeps it fast, simple, and effective. 


## Documentation

 - [Installation](#Getting-Started) 
 - [Public API Documentation](#API-Documentation) 
 - [Command Line Interface](#Command-Line-Interface) 
 - [License](#License) 
 - [Authors](#Authors)


## Getting Started

### Installing piedb

```bash
  pip install piedb

  # or update

  pip install piedb --upgrade
```

## API Documentation

 - [Database](#Database) 
 - [Collections](#Collections) 
 - [Datatypes](#Datatypes)
 - [Documents](#Documents) 
 - [Query](#Query) 
 - [Backups](#Backups) 
 - [Exceptions](#Exceptions)

## Database

### Initializing Database

When you initialize PieDB, it automatically detects an existing database or creates a new one if it doesn't exist.

```bash
  from piedb import Database

  # Default database (creates "database.json" if not found)
  db = Database()

  # Custom database (creates "mydb.json" if not found)
  db = Database("mydb")
```

Database(db_file: str = "database") -> Database

- filepath (optional, str): Name of the database file (without extension). Defaults to database.json.

- Returns: An instance of Database.

### Drop Database

```bash
  from piedb import Database

  db = Database("mydb")

  #Drops the database
  db.drop_db()
```

drop_db() -> bool

- Returns: True if the database was successfully deleted, otherwise False.


### List Database Collections

```bash
  from piedb import Database

  db = Database("mydb")

  #Drops the database
  db.list()
```

list() -> dict

- Returns: The list of existing collections and count.


## Collections

### Creating Collections

```bash
  # Create collection without schema
  db.collection("users")

  # Define schema using all supported data types
  user_schema = {
      "name": str,       # String
      "age": int,        # Integer
      "balance": float,  # Float
      "is_active": bool, # Boolean
      "address": dict,   # Dictionary
      "hobbies": list,   # List
      "created_at": datetime  # Datetime (ISO format)
  }

  # Create collection with schema
  db.collection("users", schema=user_schema)
```

collection(collection: str, schema: dict = {}) -> None

- collection (str): Name of the collection.

- schema (dict, optional): Schema definition for the collection.

- Returns: None.

### Updating Collection Schema

```bash
  # Define schema using all supported data types
  updated_schema = {
      "name": str,       # String
      "age": int,        # Integer
      "balance": float,  # Float
      "is_active": bool, # Boolean
      "address": dict,   # Dictionary
      "hobbies": list,   # List
      "created_at": datetime  # Datetime (ISO format)
  }

  # Update collection with schema
  db.set_schema("users", schema=user_schema)
```

set_schema(collection: str, schema: dict = {}) -> None

- collection (str): Name of the collection.

- schema (dict): Schema definition for the collection.

- Returns: None.

### Getting Collection Schema

```bash
  # Returns Collection Schema
  db.get_schema("users")
```
get_schema(collection: str) -> dict

- collection (str): Name of the collection.

- Returns: Schema of the collection as a dictionary.

### Getting Collection Data

```bash
  # Returns the collection data
  db.get_collection_data("users")
```

get_collection_data(collection: str) -> dict

- collection (str): Name of the collection.

- Returns: A dict including schema, documents count and latest 5 documents in the collection.

### Drop Collection

```bash
  # Drops the collection
  db.drop_collection("users")
```

drop_collection(collection: str) -> bool

- collection (str): Name of the collection to be dropped.

- Returns: True if the collection was successfully dropped, otherwise False.


## Datatypes

### Supported Datatypes

```bash
  string => "str"
  integer => "int"
  float => "float"
  boolean => "bool"
  list => "list"
  dictionay => "dict"
  datetime => "datetime"
```
## Documents

### Adding Single Document

```bash
  doc = {
      "name": "John Doe",
      "age": 24,
      "balance": 99.99,
      "is_active": True,
      "address": {
        "line 1": "ABC Road",
        "line 2": "XYZ Colony",
        "city": "Bangalore",
        "postcode": "560001" 
      },
      "hobbies": ["coding", "projects"],
      "created_at": "2025-02-22T10:10:10" # datetime.datetime.strptime("2025-02-22T10:10:10", "%Y-%m-%dT%H:%M:%S")
  }

  # Add single document to collection
  db.add("users", doc)

  '''
  RXq1wl67c0959bc #unique_id
  '''
```

add(collection: str, document: dict) -> str

- collection (str): Name of the collection.

- document (dict): The document to be inserted.

- Returns: returns unique_id(#id) for the added doc

### Adding Multiple Documents

```bash
  docs = [{
      "name": "John Doe",
      "age": 24,
      "balance": 99.99,
      "is_active": True,
      "address": {
        "line 1": "ABC Road",
        "line 2": "XYZ Colony",
        "city": "Bangalore",
        "postcode": "560001" 
      },
      "hobbies": ["coding", "projects"],
      "created_at": "2025-02-22T10:10:10" # datetime.datetime.strptime("2025-02-22T10:10:10", "%Y-%m-%dT%H:%M:%S")
  }, 
  {
      "name": "Jane Doe",
      "age": 22,
      "balance": 99.99,
      "is_active": True,
      "address": {
        "line 1": "ABC Road",
        "line 2": "XYZ Colony",
        "city": "Bangalore",
        "postcode": "560001" 
      },
      "hobbies": ["coding", "projects"],
      "created_at": "2025-02-22T10:10:10" # datetime.datetime.strptime("2025-02-22T10:10:10", "%Y-%m-%dT%H:%M:%S")
  }]

  # Add single document to collection
  db.add_many("users", docs)

  '''
  ['FEezR867c0969bc', 'z6l8l067c0969bc']
  '''
```

add_many(collection: str, documents: list) -> list

- collection (str): Name of the collection.

- documents (list): A list of documents to be inserted.

- Returns: Returns the list of list of unique_ids(#id) for the inserted docs

### Updating Documents

```bash
  updates = {
      "balance": 999.99
  }

  query = {
    "name": {"$eq": "John Doe"}
  }

  limit = 1

  # Updates document/documents on the basis of query
  # If the limit is 0, updated all the documents matching the query

  db.update("users", updates, query, limit)

  '''
  [{'name': 'John Doe', 'age': 24, 'balance': 999.99, 'is_active': True, 'address': {'line 1': 'ABC Road', 'line 2': 'XYZ Colony', 'city': 'Bangalore', 'postcode': '560001'}, 'hobbies': ['coding', 'projects'], 'created_at': '2025-02-22T10:10:10', '#id': '67c0959bclRXq1w'}]
  '''
```

update(collection: str, updates: dict, query: dict, limit: int) -> list

- collection (str): Name of the collection.

- updates (dict): Fields to update.

- query (dict): Query filter to find matching documents.

- limit (int, 0 Default): Number of documents to update (0 updates all matching documents).

Returns: The list of documents updated.

### Deleting Documents

```bash
  query = {
    "$and": [
      {"age":{"$gt": 20}}, 
      {"name":{"$eq": "John Doe"}}
    ]
  }

  limit = 1

  # Updates document/documents on the basis of query
  # If the limit is 0, updated all the documents matching the query

  db.delete("users", query, limit)

  '''
[{'name': 'John Doe', 'age': 24, 'balance': 99.99, 'is_active': True, 'address': {'line 1': 'ABC Road', 'line 2': 'XYZ Colony', 'city': 'Bangalore', 'postcode': '560001'}, 'hobbies': ['coding', 'projects'], 'created_at': '2025-02-22T10:10:10', '#id': '67c0989bcfsUUkO'}]
  '''
```
delete(collection: str, query: dict, limit: int) -> list

- collection (str): Name of the collection.

- query (dict): Query filter to find matching documents.

- limit (int): Number of documents to delete (0 deletes all matching documents).

- Returns: The list of documents deleted.

## Query

### Operators Supported

```bash
  
  # $eq => equals
  query = {
    "name": {"$eq": "John Doe"}
  }

  # $ne => not equal
  query = {
    "name": {"$ne": "Jane Doe"}
  }

  # $gt => greater than
  query = {
    "balance": {"$gt": 500}
  }

  # $lt => less than
  query = {
    "age": {"$lt": 20}
  }

  # $and => logical AND
  query = {
    "$and": [
        {"balance": {"$gt": 500}}, 
        {"age": {"$lt": 25}},
        .....
      ]
  }

  # $or => logical OR
  query = {
    "$or": [
        {"balance": {"$gt": 500}}, 
        {"age": {"$lt": 25}},
        .....
      ]
  }

```

### Querying Data

```bash

  query = {
    "$or": [
        {"balance": {"$gt": 500}}, 
        {"age": {"$lt": 25}},
        .....
      ]
  }

  limit = 5

  skip = 0

  sort = "name"

  order = "asc" # "desc"

  # Add single document to collection
  db.find("users", query, limit, skip, sort, order)
```

find(collection: str, query: dict, limit: int = None, skip: int = 0, sort: str = None, order: str = "asc") -> list

- collection (str): Name of the collection.

- query (dict): Query filter to find matching documents.

- limit (int, optional): Maximum number of documents to return (If None returns all matches).

- skip (int, optional): Number of documents to skip. Defaults to 0.

- sort (str, optional): Field name to sort results by. Defaults to None (no sorting).

- order (str, optional): Sorting order, either "asc" for ascending or "desc" for descending. Defaults to "asc".

- Returns: A list of matching documents.


## Backup

### Database Backup

```bash
  from piedb import Database

  db = Database("mydb")

  #backup database
  db.backup_db("new_backup")
```

backup_db(backup_file: str = "backup") -> str

- backup_name (str): Name for the backup file (without extension).

- Returns: Filename of the backup file created.

### Database Restore

```bash
  from piedb import Database

  db = Database("mydb")

  #restore database
  db.restore_db("new_backup")
```

restore_db(backup_file: str = "backup") -> bool

- backup_name (str): Name for the backup file (without extension).

- Returns: True if the restore was successful, otherwise False.

## Exceptions

**CollectionNotFoundError** - When the collection does not exists

**SchemaValidationError** - when a schema fails to have the supported datatypes

**DocumentValidationError** - when a document has invalid fields or missing data

**ReservedKeyError** - when the string contains reserved keys

**UnsupportedOperatorError** - when an unsupported operator is present in the query


## Command Line Interface

### Database Commands

Initialize - initializes/creates the database

```bash
>> database init db_name
>> <db_name> - required
```

Drop - drops the database

```bash
>> database drop db_name
>> <db_name> - required
```

List - lists the database collections and count

```bash
>> database list
```

### Collection Commands

Create - creates a new collection

```bash
>> collection create collection_name
>> <collection_name> - required
```

Drop - drops the collection

```bash
>> collection drop collection_name
>> <collection_name> - required
```

Set Schema - updates a new schema for the collection

```bash
>> collection set_schema collection_name '{"name":str,"age":int,"created_at":datetime}'
>> <collection_name> - required
>> <schema> - required
```

Get Schema - returns the schema for the existing collection

```bash
>> collection get_schema collection_name
>> <collection_name> - required
```

Get Data - returns the schema, the document count and the latest five documents for the collection

```bash
>> collection get_data collection_name
>> <collection_name> - required
```

### Document Commands

add - adds a document to the collection

```bash
>> document add collection_name '{"name":"John Doe","age":30,"created_at":"2025-01-01 12:12:12"}'
>> <collection_name> - required
>> <document> - required as JSON
```

add_many - adds a document to the collection

```bash
>> document add_many collection_name '[{"name":"John Doe","age":30,"created_at":"2025-01-01 12:12:12"},{"name":"Jane Doe","age":28,"created_at":"2025-01-01 12:12:12"}]'
>> <collection_name> - required
>> <document> - required as list of JSON
```

update - updates a document in the collection

```bash
>> document update collection_name '{"name":"Johnathan Doe"}' --query '{"age":{"$lt":30}}' --limit 1
>> <collection_name> - required
>> <updates> - required, updates as JSON
>> <query> - optional, query as JSON
   usage >> --query <query>
>> <limit> - optional, 0 default, count of documents to be updated, 0 for all
   usage >> --limit <limit>
```

delete - deletes a document in the collection

```bash
>> document delete collection_name --query '{"age":{"$lt":30}}' --limit 1
>> <collection_name> - required
>> <query> - optional, query as JSON
   usage >> --query <query>
>> <limit> - optional, 0 default, count of documents to be deleted, 0 for all
   usage >> --limit <limit>
```

### Querying Commands

find - queries and returns data

```bash
>> find collection_name --query '{"age":{"$lt":30}}' --limit 10 --skip 5 --sort age --order desc
>> <collection_name> - required
>> <query> - optional, query as JSON
   usage >> --query <query>
>> <limit> - optional, count of documents to be fetched
   usage >> --limit <limit>
>> <skip> - optional, count of documents to be skipped
   usage >> --skip <skip>
>> <sort> - optional, the field on which sorting needs to be applied on
   usage >> --sort <field>
>> <order> - optional, order for sorting asc/desc
   usage >> --order <asc/desc>
```

### Backup Commands

backup - backups the existing database

```bash
>> backup filename
   <filename> - required, filename for backup
```

restore - restores the data in the existing database

```bash
>> restore filename
   <filename> - required, filename for restore
```

## License

[MIT](https://choosealicense.com/licenses/mit/)


## Authors

- [Shubham Kumar Gupta](https://github.com/Shubham14243)
