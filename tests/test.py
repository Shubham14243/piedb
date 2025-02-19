import unittest
import os
import json

from piedb.db import Database
from piedb.error import CollectionNotFoundError, SchemaValidationError, DocumentValidationError, ReservedKeyError

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.test_db_file = "test_database"
        self.db = Database(self.test_db_file)

        with open(self.test_db_file, "w") as f:
            json.dump({}, f)

    def tearDown(self):
        if os.path.exists(self.test_db_file):
            os.remove(self.test_db_file)

    def test_initialization(self):
        self.assertTrue(os.path.exists(self.test_db_file))

    def test_set_and_get_schema(self):
        schema = {"name": str, "age": int}
        self.db.set_schema("users", schema)
        retrieved_schema = self.db.get_schema("users")
        self.assertEqual(schema, retrieved_schema)

    def test_collection_creation(self):
        self.db.collection("users", {"name": str})
        collections = self.db.get_collections()
        self.assertIn("users", collections["collections"])

    def test_add_document(self):
        self.db.collection("users", {"name": str, "age": int})
        doc_id = self.db.add("users", {"name": "Alice", "age": 30})
        data = self.db.get_collection_data("users")
        self.assertEqual(len(data["users"]["data"]), 1)
        self.assertEqual(data["users"]["data"][0]["#id"], doc_id)

    def test_add_many_documents(self):
        self.db.collection("users", {"name": str, "age": int})
        docs = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
        ids = self.db.add_many("users", docs)
        self.assertEqual(len(ids), 2)
        data = self.db.get_collection_data("users")
        self.assertEqual(len(data["users"]), 3)

    def test_find_documents(self):
        self.db.collection("users", {"name": str, "age": int})
        self.db.add("users", {"name": "Alice", "age": 30})
        self.db.add("users", {"name": "Bob", "age": 25})
        results = self.db.find("users", query={"age": {"$gt": 20}})
        self.assertEqual(len(results), 3)

    def test_update_documents(self):
        self.db.collection("users", {"name": str, "age": int})
        self.db.add("users", {"name": "Alice", "age": 30})
        updated = self.db.update("users", updates={"age": 35}, query={"name": "Alice"})
        self.assertEqual(updated[0]["age"], 35)

    def test_delete_documents(self):
        self.db.collection("users", {"name": str, "age": int})
        self.db.add("users", {"name": "Alice", "age": 30})
        deleted = self.db.delete("users", query={"name": "Alice"})
        self.assertEqual(len(deleted), 3)
        self.assertEqual(self.db.get_count("users"), 1)

    def test_backup(self):
        backup_file = self.db.backup_db("test_backup")
        self.assertTrue(os.path.exists(backup_file))
        os.remove(backup_file)

    def test_reserved_key_error(self):
        with self.assertRaises(ReservedKeyError):
            self.db.collection("_counts")

    def test_collection_not_found_error(self):
        with self.assertRaises(CollectionNotFoundError):
            self.db.get_collection_data("nonexistent")

    def test_schema_validation_error(self):
        self.db.collection("users", {"name": str, "age": int})
        with self.assertRaises(SchemaValidationError):
            self.db.add("users", {"name": "Alice"})

    def test_document_validation_error(self):
        self.db.collection("users", {"name": str, "age": int})
        with self.assertRaises(DocumentValidationError):
            self.db.add("users", {"name": "Alice", "age": "thirty"})

if __name__ == "__main__":
    unittest.main()