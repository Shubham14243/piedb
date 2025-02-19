
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


## Getting Started

Installing piedb

```bash
  pip install piedb --upgrade
```

Initializing Database

When you initialize PieDB, it automatically detects an existing database or creates a new one if it doesn't exist.

```bash
  from piedb import Database

  # Default database (creates "database.json" if not found)
  db = Database()

  # Custom database (creates "mydb.json" if not found)
  db = Database("mydb")
```
## Working with Collections

Creating Collections

```bash
  # Create collection without schema
  db.collection("users")
```

Updating Collection Schema

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