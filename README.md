
# PieDB

Simple, Fast, and Lightweight Data Storage.

Tired of setting up complex databases for small projects? PieDB gives you a hassle-free way to store and manage structured data using just a JSON file. It is here to keep things simple. Designed for speed and efficiency, it lets you store and retrieve structured data effortlessly—no setup, no hassle.

With zero dependencies and a clean API, PieDB lets you:

✅ Create collections with/without schemas – Enforce structure or keep it flexible.

✅ Easy CRUD – No SQL, no headaches, just simple Python objects.

✅ Query like a pro – Use conditions ($gt, $lt, $eq, $ne), sorting, and pagination.

✅ Multi-threading support – Handles concurrent access safely.

✅ Automatic backups – Never lose your data.

Whether you're building a small app, prototyping, or need a lightweight alternative to traditional databases, PieDB keeps it fast, simple, and effective. 🚀


## Documentation

 - [Installation](#Getting-Started) 
 - [Collections](#Collections) 
 - [Datatypes](#Datatypes) 
 - [Documents](#Documents) 
 - [Query](#Query)
 - [Exceptions](#Exceptions)
## Getting-Started

### Installing piedb

```bash
  pip install piedb

  # or update

  pip install piedb --upgrade
```

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

### Database Backup

```bash
  from piedb import Database

  db = Database("mydb")

  #backup database
  db.backup_db("new_backup")
```

backup_db(backup_file: str = "backup") -> bool

- backup_name (str): Name for the backup file (without extension).

- Returns: True if the backup was successful, otherwise False.

### Deleting Database

```bash
  from piedb import Database

  db = Database("mydb")

  #Deletes database
  db.delete_db()
```

delete_db() -> bool

- Returns: True if the database was successfully deleted, otherwise False.
## Collections

### Creating Collections

```bash
  # Create collection without schema
  db.collection("users")
```

collection(collection: str, schema: dict = None) -> None

- collection (str): Name of the collection.

- schema (optional, dict): Schema definition for the collection.

- Returns: None.

### Updating Collection Schema

```bash
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

  # Create/Update collection with schema
  db.collection("users", schema=user_schema)
```

collection(collection: str, schema: dict = None) -> None

- collection (str): Name of the collection.

- schema (optional, dict): Schema definition for the collection.

- Returns: None.

### Getting Collection Schema

```bash
  # Returns Collection Schema
  db.get_schema("users")
```

get_schema(collection: str) -> dict

collection (str): Name of the collection.

Returns: Schema of the collection as a dictionary.

### Getting All Collections

```bash
  # Returns all the collections
  db.get_collections()
```
get_collections() -> dict

- Returns: A dict including list collection names and their count.

### Getting Collection Data

```bash
  # Returns the collection data
  db.get_collection_data("users")
```

get_collection_data(collection: str) -> dict

collection (str): Name of the collection.

Returns: A dict including schema, count and latest 5 documents in the collection.

### Delete Collection

```bash
  # Deletes the collection
  db.delete_collection("users")
```

delete_collection(collection: str) -> bool

collection (str): Name of the collection to be deleted.

Returns: True if the collection was successfully deleted, otherwise False.
## Datatypes

### Supported Datatypes

```bash
  string => "str"
  integer => "int"
  float => "float"
  boolean => "bool"
  datetime => "datetime"
  dictionay => "dict"
  list => "list"
```
## Documents

### Adding Single Document

```bash
  doc = {
      "name": "John Doe",
      "age": 24,
      "balance": 99.99,
      "is_active": true,
      "address": {
        "line 1": "ABC Road",
        "line 2": "XYZ Colony",
        "city": "Bangalore",
        "postcode": "560001" 
      },
      "hobbies": ["coding", "projects"]
      "created_at": "2025-02-22T10:10:10" # datetime.datetime.strptime("2025-02-22T10:10:10", "%Y-%m-%dT%H:%M:%S")
  }

  # Add single document to collection
  db.add("users", doc)
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
      "is_active": true,
      "address": {
        "line 1": "ABC Road",
        "line 2": "XYZ Colony",
        "city": "Bangalore",
        "postcode": "560001" 
      },
      "hobbies": ["coding", "projects"]
      "created_at": "2025-02-22T10:10:10" # datetime.datetime.strptime("2025-02-22T10:10:10", "%Y-%m-%dT%H:%M:%S")
  }, 
  {
      "name": "Jane Doe",
      "age": 22,
      "balance": 99.99,
      "is_active": true,
      "address": {
        "line 1": "ABC Road",
        "line 2": "XYZ Colony",
        "city": "Bangalore",
        "postcode": "560001" 
      },
      "hobbies": ["coding", "projects"]
      "created_at": "2025-02-22T10:10:10" # datetime.datetime.strptime("2025-02-22T10:10:10", "%Y-%m-%dT%H:%M:%S")
  }]

  # Add single document to collection
  db.add_many("users", docs)
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
```

update(collection: str, updates: dict, query: dict, limit: int) -> list

- collection (str): Name of the collection.

- updates (dict): Fields to update.

- query (dict): Query filter to find matching documents.

- limit (int): Number of documents to update (0 updates all matching documents).

Returns: The list of documents updated.

### Deleting Documents

```bash
  query = {
    "$and": [
      ("age", {"$gt": 20}), 
      ("name", {"$eq": "John Doe"})
    ]
  }

  limit = 1

  # Updates document/documents on the basis of query
  # If the limit is 0, updated all the documents matching the query

  db.delete("users", query, limit)
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
        ("balance": {"$gt": 500}), 
        ("age", {"$lt": 25}),
        .....
      ]
  }

  # $or => logical OR
  query = {
    "$or": [
        ("balance": {"$gt": 500}), 
        ("age", {"$lt": 25}),
        .....
      ]
  }

```

### Querying Data

```bash

  query = {
    "$or": [
        ("balance": {"$gt": 500}), 
        ("age", {"$lt": 25}),
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

skip (int, optional): Number of documents to skip. Defaults to 0.

sort (str, optional): Field name to sort results by. Defaults to None (no sorting).

order (str, optional): Sorting order, either "asc" for ascending or "desc" for descending. Defaults to "asc".

Returns: A list of matching documents.
## Exceptions

**CollectionNotFoundError** - When the collection does not exists

**SchemaValidationError** - when a document does not conform to the collection's schema

**DocumentValidationError** - when a document has invalid fields or missing data

**ReservedKeyError** - when the string contains reserved keys - _schemas and _counts