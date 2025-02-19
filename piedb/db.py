import json
import os
from datetime import datetime
from threading import RLock

from .util import Utility
from .util import CustomJSONEncoder
from .error import CollectionNotFoundError
from .error import SchemaValidationError
from .error import DocumentValidationError
from .error import ReservedKeyError


class Database:
    
    
    def __init__(self, db_file: str ="database") -> None:
        """Initialize the Database"""
        
        self.EXT = ".json"
        self.db_file = db_file + self.EXT
        self.lock = RLock()
        self.SKELETON = {"_counts": {}, "_schemas": {}}
        self.RESERVED_KEYS = ["_schemas", "_counts"]
        
        if not os.path.exists(self.db_file):
            with open(self.db_file, "w") as f:
                json.dump(self.SKELETON, f, indent=4)


    def _read_db(self) -> None:
        """Read the database from the file."""
        
        with self.lock:
            with open(self.db_file, "r") as f:
                return json.load(f)


    def _write_db(self, data: dict) -> None:
        """Write the database to the file."""
        
        with self.lock:
            with open(self.db_file, "w") as f:
                json.dump(data, f, indent=4, cls=CustomJSONEncoder)


    def delete_db(self) -> None:
        """Delete the entire database file."""
        
        with self.lock:
            if os.path.exists(self.db_file):
                os.remove(self.db_file)


    def set_schema(self, collection: str, schema: dict={}) -> None:
        """Define a schema for a collection."""
        with self.lock:
            self._validate_collection_exists(collection)
            
            schema_str = Utility._type_to_string(schema)
                
            db = self._read_db()
            db["_schemas"][collection] = schema_str
            self._write_db(db)


    def get_schema(self, collection: str) -> dict:
        """Retrieve the schema for a collection."""
        
        db = self._read_db()
        schema = db.get("_schemas", {}).get(collection)
            
        return Utility._string_to_type(schema) if schema else None
    
    
    def _set_count(self, collection: str) -> None:
        """Initialize or Update the count for a collection."""
        with self.lock:
            db = self._read_db()
            db["_counts"][collection] = len(db[collection])
            self._write_db(db)
    
    
    def get_count(self, collection: str) -> int:
        """Retrieve the count for a collection."""
        
        with self.lock:
            db = self._read_db()
            count = db.get("_counts", {}).get(collection)
            return count


    def _validate_collection_exists(self, collection: str) -> None:
        """Check if a collection exists in the database."""
        
        db = self._read_db()
        if collection in self.RESERVED_KEYS:
            raise ReservedKeyError()
        if collection not in db:
            raise CollectionNotFoundError(collection)


    def collection(self, collection: str, schema: dict =None) -> None:
        """Create a new collection with a schema."""
        
        if collection in self.RESERVED_KEYS:
            raise ReservedKeyError()
        else:
            with self.lock:
                db = self._read_db()
                if collection not in db:
                    db[collection] = []
                    self._write_db(db)
                    
                    if schema == None:
                        schema = {}
                        
                    self.set_schema(collection, schema)
                    self._set_count(collection)


    def get_collections(self) -> dict:
        """Return a dict of all collections."""
        
        db = self._read_db()
        collections = list(db["_schemas"].keys())
        count = len(collections)
        return {"collections": collections, "count": count}


    def delete_collection(self, collection: str) -> None:
        """Delete a collection."""

        with self.lock:
            try:
                self._validate_collection_exists(collection)

                db = self._read_db()
                db["_schemas"].pop(collection, None)
                db["_counts"].pop(collection, None)
                db.pop(collection, None)
                self._write_db(db)
                
            except Exception as e:
                raise e
        
    
    def get_collection_data(self, collection: str) -> dict:
        """Get a collection's data."""
        
        with self.lock:
            self._validate_collection_exists(collection)
            
            db = self._read_db()
            collection_schema = db["_schemas"][collection]
            collection_count = db["_counts"][collection]
            data = db[collection][:5]
            return {collection: {"_schema": collection_schema, "count": collection_count, "data": data}}


    def _validate_document(self, collection: str, document: dict) -> bool:
        """Validate a document against the collection's schema."""
        
        schema = self.get_schema(collection)
        if not schema:
            return True

        for field, field_type in schema.items():
            if field not in document:
                raise SchemaValidationError(f"Missing required field: {field}")
            
            if field_type is datetime:
                if not isinstance(document[field], (str, datetime)):
                    raise DocumentValidationError(f"Field '{field}' must be a datetime object or a string in ISO format.")
                if isinstance(document[field], str):  # Convert string to datetime
                    try:
                        document[field] = datetime.fromisoformat(document[field])
                    except ValueError:
                        raise DocumentValidationError(f"Field '{field}' must be a valid ISO 8601 datetime string.")
            elif not isinstance(document[field], field_type):
                raise DocumentValidationError(f"Field '{field}' must be of type {field_type.__name__}.")
        return True


    def add(self, collection: str, document: dict) -> str:
        """Add a new document to a collection."""
        
        with self.lock:
            self._validate_collection_exists(collection)
            
            db = self._read_db()

            try:
                self._validate_document(collection, document)
            except (SchemaValidationError, DocumentValidationError) as e:
                raise e

            unique_id = Utility.generate_id(collection)
            document.setdefault("#id", unique_id)
            db[collection].append(document)
        
            self._write_db(db)
            
            self._set_count(collection)

            return unique_id


    def add_many(self, collection: str, documents: list) -> list:
        """Add multiple new documents to a collection."""
        
        with self.lock:
            self._validate_collection_exists(collection)
            
            db = self._read_db()
            added_ids = []

            for document in documents:
                try:
                    self._validate_document(collection, document)
                    unique_id = Utility.generate_id(collection)
                    document.setdefault("#id", unique_id)
                    db[collection].append(document)
                    added_ids.append(unique_id)
                except (SchemaValidationError, DocumentValidationError) as e:
                    raise e
            
            self._write_db(db)
            self._set_count(collection)

            return added_ids


    def _evaluate_condition(self, doc_value: any, condition: dict) -> bool:
        """Evaluate a condition (support for $gt, $lt, $ne, $eq)."""
        
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
                    return False
        else:
            return doc_value == condition
        return True


    def find(self, collection: str, query: dict =None, limit: int =None, skip: int =0, sort: str =None, order: str ="asc") -> list:
    
        with self.lock:
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
                            match = any(self._evaluate_condition(doc.get(cond[0]), cond[1]) for cond in v)
                        elif k == '$and' and isinstance(v, list):
                            match = all(self._evaluate_condition(doc.get(cond[0]), cond[1]) for cond in v)
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
        
        with self.lock:
            self._validate_collection_exists(collection)
            
            updated_count = 0
            updated_documents = []
            
            if self.get_count(collection) <= 0:
                return updated_documents
            
            if query is None:
                query = {}
                
            db = self._read_db()

            for doc in db[collection]:
                
                if limit != 0 and updated_count >= limit:
                    break
                
                if all(self._evaluate_condition(doc.get(k), v) for k, v in query.items()):
                    updated_doc = {**doc, **updates}
                    try:
                        self._validate_document(collection, updated_doc)
                    except (SchemaValidationError, DocumentValidationError) as e:
                        raise e
                    doc.update(updates)
                    updated_count += 1
                    updated_documents.append(doc)

            self._write_db(db)
            return updated_documents


    def delete(self, collection: str, query: dict =None, limit: int =0) -> list:
        """Delete the first document from a collection that matches the query, or the first document if no query is provided."""
        
        with self.lock:
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
                    deleted_docs = collection_data[-limit:]
                    db[collection] = collection_data[:-limit]
            
            else:
                to_delete = []
                for doc in reversed(collection_data):
                    if all(
                        self._evaluate_condition(doc.get(k), v) if isinstance(v, dict) else doc.get(k) == v
                        for k, v in query.items()
                    ):
                        to_delete.append(doc)
                        if limit > 0 and len(to_delete) >= limit:
                            break

                deleted_docs = to_delete
                for doc in to_delete:
                    collection_data.remove(doc)
            
            db[collection] = collection_data
            self._write_db(db)
            self._set_count(collection)

            return deleted_docs


    def backup_db(self, backup_file: str ="backup") -> str:
        """Create a backup of the database."""
        
        with self.lock:

            if not os.path.exists(self.db_file):
                raise FileNotFoundError(f"Database file '{self.db_file}' does not exist.")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{backup_file}_{timestamp}.json"

            backup_dir = os.path.dirname(backup_file)
            if backup_dir and not os.path.exists(backup_dir):
                os.makedirs(backup_dir)

            try:
                with open(self.db_file, "r") as original, open(backup_filename, "w") as backup:
                    backup.write(original.read())
            except FileNotFoundError:
                raise FileNotFoundError(f"Original database file '{self.db_file}' not found.")
            except Exception as e:
                raise RuntimeError(f"An error occurred during backup: {e}")

            return backup_filename
