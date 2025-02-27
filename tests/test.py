import unittest
import os
import json
from datetime import datetime
from piedb import Database
from piedb.error import CollectionNotFoundError, DocumentValidationError, ReservedKeyError


class TestDatabase(unittest.TestCase):
    
    def setUp(self):
        """Initialize the test database file."""
        self.db = Database("test_db")
        
    def tearDown(self):
        """Clean up test database file after each test."""
        if os.path.exists(self.db.db_file):
            os.remove(self.db.db_file)
    
    def test_create_collection(self):
        """Test creating a collection."""
        self.db.collection("users", {"name": str, "age": int})
        collections = self.db.get_collections()
        self.assertIn("users", collections["collections"])

    def test_add_document(self):
        """Test adding a document to a collection."""
        self.db.collection("users", {"name": str, "age": int})
        doc_id = self.db.add("users", {"name": "John", "age": 30})
        self.assertIsInstance(doc_id, str)

    def test_add_invalid_document(self):
        """Test adding an invalid document (wrong schema)."""
        self.db.collection("users", {"name": str, "age": int})
        with self.assertRaises(DocumentValidationError):
            self.db.add("users", {"name": "John", "age": "thirty"})
    
    def test_update_document(self):
        """Test updating a document in a collection."""
        self.db.collection("users", {"name": str, "age": int})
        self.db.add("users", {"name": "Alice", "age": 25})
        updated_docs = self.db.update("users", {"age": 26}, {"name": "Alice"})
        self.assertEqual(updated_docs[0]["age"], 26)
    
    def test_find_documents(self):
        """Test finding documents in a collection."""
        self.db.collection("users", {"name": str, "age": int})
        self.db.add("users", {"name": "Bob", "age": 40})
        self.db.add("users", {"name": "Charlie", "age": 35})
        results = self.db.find("users", {"age": {"$gt": 30}})
        self.assertEqual(len(results), 2)
    
    def test_delete_document(self):
        """Test deleting a document from a collection."""
        self.db.collection("users", {"name": str, "age": int})
        self.db.add("users", {"name": "David", "age": 45})
        deleted_docs = self.db.delete("users", {"name": "David"})
        self.assertEqual(len(deleted_docs), 1)

    def test_backup_database(self):
        """Test creating a backup of the database."""
        backup_file = self.db.backup_db("test_db_backup")
        self.assertTrue(os.path.exists(backup_file))
        os.remove(backup_file)

if __name__ == "__main__":
    unittest.main()
