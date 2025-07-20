import os
import json
from threading import RLock
from datetime import datetime

from .util import Utility
from .util import CustomJSONEncoder
from .error import CollectionNotFoundError
from .error import DocumentValidationError
from .error import ReservedKeyError
from .error import UnsupportedOperatorError


class Database:
    
    
    def __init__(self, db_file: str ="database") -> None:
        """Initialize the Database"""
        
        self.EXT = ".json"
        self.VERSION = "2.0.0"
        
        self.DB_FILE = db_file
        if not db_file.endswith(self.EXT):
            self.DB_FILE = db_file + self.EXT
        self.PATH = os.getcwd()
        self.LOCK = RLock()

        self.SKELETON = {"_meta": {"_version": self.VERSION, "_path": self.PATH, "_count": {}, "_schema": {}}}
        self.RESERVED_KEYS = ["_meta", "_version", "_path", "_count", "_schema", "_id_"]

        if not os.path.exists(self.DB_FILE):
            with open(self.DB_FILE, "w") as f:
                json.dump(self.SKELETON, f, indent=4)


    def _read_db(self) -> dict:
        """Read the database from the file."""
        
        with self.LOCK:
            with open(self.DB_FILE, "r") as f:
                return json.load(f)


    def _write_db(self, data: dict) -> None:
        """Write the database to the file."""
        
        with self.LOCK:
            with open(self.DB_FILE, "w") as f:
                json.dump(data, f, indent=4, cls=CustomJSONEncoder)


    def drop_db(self) -> bool:
        """Delete the entire database file."""
        
        with self.LOCK:
            if os.path.exists(self.DB_FILE):
                os.remove(self.DB_FILE)
                return True
        return False


    def list(self) -> dict:
        """Return a dict of all collections."""
        
        db = self._read_db()
        collections = list(db.keys())
        count = len(collections) - 1
        return {"collections": collections[1:], "count": count}


    def set_schema(self, collection: str, schema: dict={}) -> None:
        """Define a schema for a collection."""
        with self.LOCK:
            self._validate_collection_exists(collection)
            
            schema_str = Utility._type_to_string(schema)
                
            db = self._read_db()
            db["_meta"]["_schema"][collection] = schema_str
            self._write_db(db)


    def get_schema(self, collection: str) -> dict:
        """Retrieve the schema for a collection."""
        
        db = self._read_db()
        schema = db.get("_meta", {}).get("_schema", {}).get(collection, None)
        
        if schema is None:
            return {}
            
        return Utility._string_to_type(schema)
    
    
    def _set_count(self, collection: str) -> None:
        """Initialize or Update the count for a collection."""
        with self.LOCK:
            db = self._read_db()
            db["_meta"]["_count"][collection] = len(db[collection])
            self._write_db(db)
    
    
    def get_count(self, collection: str) -> int:
        """Retrieve the count for a collection."""
        
        self._validate_collection_exists(collection)
        
        with self.LOCK:
            db = self._read_db()
            count = db.get("_meta", {}).get("_count", {}).get(collection, 0)
            return count


    def _validate_collection_exists(self, collection: str) -> None:
        """Check if a collection exists in the database."""
        
        db = self._read_db()
        if collection in self.RESERVED_KEYS:
            raise ReservedKeyError()
        if collection not in db:
            raise CollectionNotFoundError(collection)


    def collection(self, collection: str, schema: dict = {}) -> None:
        """Create a new collection with a schema."""
        
        if collection in self.RESERVED_KEYS:
            raise ReservedKeyError()
        else:
            flag = False
            with self.LOCK:
                db = self._read_db()
                if collection not in db:
                    flag = True
                    db[collection] = []
                    self._write_db(db)
            if flag == True:                            
                self.set_schema(collection, schema)
                self._set_count(collection)


    def drop_collection(self, collection: str) -> bool:
        """Delete a collection."""

        with self.LOCK:
            try:
                self._validate_collection_exists(collection)

                db = self._read_db()
                db["_meta"]["_schema"].pop(collection, None)
                db["_meta"]["_count"].pop(collection, None)
                db.pop(collection, None)
                self._write_db(db)
                return True
                
            except Exception as e:
                raise e
        return False
        
    
    def get_collection_data(self, collection: str) -> dict:
        """Get a collection's data."""
        
        with self.LOCK:
            self._validate_collection_exists(collection)
            
            db = self._read_db()
            collection_schema = db["_meta"]["_schema"][collection]
            collection_count = db["_meta"]["_count"][collection]
            data = db[collection][:5]
            return {collection: {"_schema": collection_schema, "count": collection_count, "data": data}}


    def _validate_document(self, collection: str, document: dict) -> bool:
        """Validate a document against the collection's schema."""
        
        for key in document.keys():
            if key in self.RESERVED_KEYS:
                raise ReservedKeyError(f"'{key}' {self.RESERVED_KEYS} are reserved keys.")
        
        schema = self.get_schema(collection)
        if not schema:
            return True

        for field, field_type in schema.items():
            if field not in document:
                raise DocumentValidationError(f"Missing required field: {field}")
            
            if field_type is datetime:
                if not isinstance(document[field], (str, datetime)):
                    raise DocumentValidationError(f"Field '{field}' must be a datetime object or a string in ISO format.")
                if isinstance(document[field], str):
                    try:
                        document[field] = datetime.fromisoformat(document[field])
                    except ValueError:
                        raise DocumentValidationError(f"Field '{field}' must be a valid ISO 8601 datetime string.")
            elif not isinstance(document[field], field_type):
                raise DocumentValidationError(f"Field '{field}' must be of type {field_type.__name__}.")
        return True


    def add(self, collection: str, document: dict) -> str:
        """Add a new document to a collection."""
        
        with self.LOCK:
            self._validate_collection_exists(collection)
            
            db = self._read_db()

            try:
                self._validate_document(collection, document)
            except DocumentValidationError as e:
                raise e

            unique_id = Utility.generate_id(collection)
            document.setdefault("_id", unique_id)
            db[collection].append(document)
        
            self._write_db(db)
            
            self._set_count(collection)

            return unique_id


    def add_many(self, collection: str, documents: list) -> list:
        """Add multiple new documents to a collection."""
        
        with self.LOCK:
            self._validate_collection_exists(collection)
            
            db = self._read_db()
            added_ids = []

            for document in documents:
                try:
                    self._validate_document(collection, document)
                    unique_id = Utility.generate_id(collection)
                    document.setdefault("_id", unique_id)
                    db[collection].append(document)
                    added_ids.append(unique_id)
                except DocumentValidationError as e:
                    raise e
            
            self._write_db(db)
            self._set_count(collection)

            return added_ids


    def _evaluate_condition(self, doc_value: any, condition: dict) -> bool:
        """Evaluate a condition (support for $gt, $lt, $ne, $eq)."""
        
        if doc_value is None:
            return False
        
        if isinstance(condition, dict):
            for operator, value in condition.items():
                if operator == '$gt':
                    if not doc_value > value:
                        return False
                elif operator == '$lt':
                    if not doc_value < value:
                        return False
                elif operator == '$eq':
                    if not doc_value == value:
                        return False
                elif operator == '$ne':
                    if not doc_value != value:
                        return False
                else:
                    raise UnsupportedOperatorError(operator)
        else:
            return doc_value == condition
        return True


    def find(self, collection: str, query: dict =None, limit: int =None, skip: int =0, sort: str =None, order: str ="asc") -> list:
    
        with self.LOCK:
            self._validate_collection_exists(collection)
            db = self._read_db()

            if not query:
                documents = db[collection]
            else:
                documents = []
                for doc in db[collection]:
                    match = True
                    for k, v in query.items():
                        if k == '$or' and isinstance(v, list):
                            match = any(
                                all(self._evaluate_condition(doc.get(field), cond) for field, cond in subquery.items())
                                for subquery in v
                            )
                        elif k == '$and' and isinstance(v, list):
                            match = all(
                                all(self._evaluate_condition(doc.get(field), cond) for field, cond in subquery.items())
                                for subquery in v
                            )
                        else:
                            match = self._evaluate_condition(doc.get(k), v)

                        if not match:
                            break

                    if match:
                        documents.append(doc)

            if sort:
                reverse = order.lower() == "desc"
                documents.sort(key=lambda x: x.get(sort) if sort in x else float('inf'), reverse=reverse)

            documents = documents[skip:] if limit is None else documents[skip:skip + limit]

            return documents


    def update(self, collection: str, updates: dict, query: dict =None, limit: int =0) -> list:
        """Update all documents in a collection that match the query."""
        
        with self.LOCK:
            self._validate_collection_exists(collection)
            
            updated_count = 0
            updated_documents = []
            
            if self.get_count(collection) <= 0:
                return updated_documents
            
            if query is None:
                query = {}
                
            db = self._read_db()
            collection_data = db[collection]

            for doc in collection_data:
                if updated_count >= limit and limit > 0:
                    break

                match = True
                for k, v in query.items():
                    if k == '$or' and isinstance(v, list):
                        match = any(
                            all(self._evaluate_condition(doc.get(field), cond) for field, cond in subquery.items())
                            for subquery in v
                        )
                    elif k == '$and' and isinstance(v, list):
                        match = all(
                            all(self._evaluate_condition(doc.get(field), cond) for field, cond in subquery.items())
                            for subquery in v
                        )
                    else:
                        match = self._evaluate_condition(doc.get(k), v)

                    if not match:
                        break

                if match:
                    updated_doc = {**doc, **updates}
                    try:
                        self._validate_document(collection, updated_doc)
                    except DocumentValidationError as e:
                        raise e
                    doc.update(updates)
                    updated_count += 1
                    updated_documents.append(doc)

            self._write_db(db)
            return updated_documents


    def delete(self, collection: str, query: dict = None, limit: int = 0) -> list:
        """Delete documents from a collection that match the query. If no query is provided, delete the first N documents (or all if limit=0)."""

        with self.LOCK:
            self._validate_collection_exists(collection)

            if self.get_count(collection) <= 0:
                return []

            deleted_docs = []
            db = self._read_db()
            collection_data = db[collection]

            if query is None:
                if limit == 0:
                    deleted_docs = collection_data[:]
                    db[collection] = []
                else:
                    deleted_docs = collection_data[:limit]  # ✅ Delete first N
                    db[collection] = collection_data[limit:]
            else:
                new_data = []
                matched_count = 0

                for doc in collection_data:
                    if limit > 0 and matched_count >= limit:
                        new_data.append(doc)
                        continue

                    match = True
                    for k, v in query.items():
                        if k == '$or' and isinstance(v, list):
                            match = any(
                                all(self._evaluate_condition(doc.get(field), cond) for field, cond in subquery.items())
                                for subquery in v
                            )
                        elif k == '$and' and isinstance(v, list):
                            match = all(
                                all(self._evaluate_condition(doc.get(field), cond) for field, cond in subquery.items())
                                for subquery in v
                            )
                        else:
                            match = self._evaluate_condition(doc.get(k), v)

                        if not match:
                            break

                    if match:
                        deleted_docs.append(doc)
                        matched_count += 1
                    else:
                        new_data.append(doc)

                db[collection] = new_data

            self._write_db(db)
            self._set_count(collection)

            return deleted_docs


    def backup_db(self, backup_file: str ="backup") -> str:
        """Create a backup of the database."""
        
        with self.LOCK:

            if not os.path.exists(self.DB_FILE):
                raise FileNotFoundError(f"Database file '{self.DB_FILE}' does not exist.")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{backup_file}_{timestamp}.json"

            backup_dir = os.path.dirname(backup_file)
            if backup_dir and not os.path.exists(backup_dir):
                os.makedirs(backup_dir)

            try:
                with open(self.DB_FILE, "r") as original, open(backup_filename, "w") as backup:
                    backup.write(original.read())
            except FileNotFoundError:
                raise FileNotFoundError(f"Original database file '{self.DB_FILE}' not found.")
            except Exception as e:
                raise RuntimeError(f"An error occurred during backup: {e}")

            return backup_filename
        
    
    def restore_db(self, backup_file_path: str) -> bool:
        """Restore the database from a backup file."""

        if not backup_file_path.endswith(self.EXT):
            backup_file_path += self.EXT

        with self.LOCK:
            if not os.path.exists(backup_file_path):
                raise FileNotFoundError(f"Backup file '{backup_file_path}' does not exist.")

            with open(backup_file_path, "r") as f:
                backup_db = json.load(f)

            db = self._read_db()

            backup_meta = backup_db.get("_meta", {})
            backup_schemas = backup_meta.get("_schema", {})

            for collection_name, docs in backup_db.items():

                if collection_name == "_meta":
                    continue

                backup_schema = backup_schemas.get(collection_name, {})

                if collection_name not in db:
                    self.collection(collection_name, Utility._string_to_type(backup_schema))

                    for doc in docs:
                        self.add(collection_name, doc)
                    
                    print(f"Restored collection '{collection_name}' with {len(docs)} documents.")

                else:
                    existing_schema = self.get_schema(collection_name)

                    # Convert existing schema to string for comparison
                    existing_schema_str = Utility._type_to_string(existing_schema)

                    existing_normalized = Utility._normalize_schema(existing_schema_str)
                    backup_normalized = Utility._normalize_schema(backup_schema)

                    if existing_normalized == backup_normalized:
                        for doc in docs:
                            self.add(collection_name, doc)
                        print(f"Appended {len(docs)} documents to existing collection '{collection_name}'.")
                    else:
                        new_name = Utility.unique_collection_name(collection_name, db)
                        self.collection(new_name, Utility._string_to_type(backup_schema))

                        for doc in docs:
                            self.add(new_name, doc)

                        print(f"Created new collection '{new_name}' due to schema mismatch. Inserted {len(docs)} documents.")

            print("Restore completed successfully.")
            return True
        return False
