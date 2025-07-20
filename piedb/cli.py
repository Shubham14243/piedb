import os
import json
import shlex
import argparse
from datetime import datetime
from beautifultable import BeautifulTable

from .db import Database

def main():
    
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="PieDB CLI - A simple JSON database CLI", prog="PieDB CLI")
    
    subparsers = parser.add_subparsers(dest='command')
    
    
    # Database commands
    
    parser_db = subparsers.add_parser('database', help='Database Operations')
    db_subparsers = parser_db.add_subparsers(dest='db_command')

    parser_db_init = db_subparsers.add_parser('init', help='Initialize a new database')
    parser_db_init.add_argument('db_name', type=str, help='The name of the database to initialize')

    parser_db_drop = db_subparsers.add_parser('drop', help='Drop the database')
    parser_db_drop.add_argument('db_name', type=str, help='The name of the database to drop')

    parser_db_list = db_subparsers.add_parser('list', help='List all collections in the database')
    
    # Collection commands
    
    parser_collection = subparsers.add_parser('collection', help='Collection Operations')
    collection_subparsers = parser_collection.add_subparsers(dest='collection_command')
    
    parser_collection_create = collection_subparsers.add_parser('create', help='Create a new collection')
    parser_collection_create.add_argument('collection_name', type=str, help='Name of the collection to create')

    parser_collection_drop = collection_subparsers.add_parser('drop', help='Drop a collection')
    parser_collection_drop.add_argument('collection_name', type=str, help='Name of the collection to drop')

    parser_collection_set_schema = collection_subparsers.add_parser('set_schema', help='Set schema for a collection')
    parser_collection_set_schema.add_argument('collection_name', type=str, help='Name of the collection')
    parser_collection_set_schema.add_argument('schema', type=str, help='Schema for the collection in JSON format')
    
    parser_collection_get_schema = collection_subparsers.add_parser('get_schema', help='Get schema of a collection')
    parser_collection_get_schema.add_argument('collection_name', type=str, help='Name of the collection')
    
    parser_collection_get_data = collection_subparsers.add_parser('get_data', help='Get data from a collection')
    parser_collection_get_data.add_argument('collection_name', type=str, help='Name of the collection')
    
    
    #Document commands
    
    parser_document = subparsers.add_parser('document', help='Document Operations')
    document_subparsers = parser_document.add_subparsers(dest='document_command')
    
    parser_document_add = document_subparsers.add_parser('add', help='Add a document to a collection')
    parser_document_add.add_argument('collection_name', type=str, help='Name of the collection')
    parser_document_add.add_argument('document', type=str, help='Document to add in JSON format')
    
    parser_document_add_many = document_subparsers.add_parser('add_many', help='Add multiple documents to a collection')
    parser_document_add_many.add_argument('collection_name', type=str, help='Name of the collection')
    parser_document_add_many.add_argument('documents', type=str, help='Documents to add in JSON format')
    
    parser_document_update = document_subparsers.add_parser('update', help='Update documents in a collection')
    parser_document_update.add_argument('collection_name', type=str, help='Name of the collection')
    parser_document_update.add_argument('update', type=str, help='Update operations in JSON format')
    parser_document_update.add_argument('query', type=str, help='Query to match documents')
    parser_document_update.add_argument('--limit', type=int, default=0, help='Update multiple documents')
    
    parser_document_delete = document_subparsers.add_parser('delete', help='Delete documents from a collection')
    parser_document_delete.add_argument('collection_name', type=str, help='Name of the collection')
    parser_document_delete.add_argument('query', type=str, help='Query to match documents')
    parser_document_delete.add_argument('--limit', type=int, default=0, help='Delete multiple documents')
    
    #Find command
    
    parser_find = subparsers.add_parser('find', help='Find documents in a collection')
    parser_find.add_argument('collection_name', type=str, help='Name of the collection')
    parser_find.add_argument('--query', type=str, default=None, help='Query to match documents')
    parser_find.add_argument('--limit', type=int, default=None, help='Limit the number of documents returned')
    parser_find.add_argument('--skip', type=int, default=0, help='Number of documents to skip')
    parser_find.add_argument('--sort', type=str, default=None, help='Field for sorting the results')
    parser_find.add_argument('--order', type=str, default="asc", help='Sort order for the results')
    
    #Backup command

    parser_backup = subparsers.add_parser('backup', help='Backup the database')
    parser_backup.add_argument('backup_file', type=str, help='Path to the backup file')
    
    parser_restore = subparsers.add_parser('restore', help='Restore the database from a backup')
    parser_restore.add_argument('backup_file', type=str, help='Path to the backup file')

    print('############### PieDB CLI! ###############\nType "exit" to quit cli.')

    DATABASE = None

    while True:
        try:
            line = input('piedb>> ')
            if not line.strip():
                continue
            if line.strip() in ['exit']:
                print('############### EXIT! ###############')
                break

            if line.strip() == 'clear':
                os.system('cls' if os.name == 'nt' else 'clear')
                continue

            args = parser.parse_args(shlex.split(line))

            if args.command == 'database':
                if args.db_command == 'init':
                    db_name = args.db_name
                    db = Database(db_name)
                    DATABASE = db
                    print(f"Database '{db_name}' initialized.")

                elif args.db_command == 'drop':
                    if DATABASE is None:
                        print("No database initialized. Please initialize a database first.")
                        continue
                    db_name = args.db_name
                    if DATABASE.DB_FILE != db_name + DATABASE.EXT:
                        print(f"Confirm database name to drop: {db_name}")
                        continue
                    result = DATABASE.drop_db()
                    print(f"Database '{db_name}' dropped.")

                elif args.db_command == 'list':
                    if DATABASE is None:
                        print("No database initialized. Please initialize a database first.")
                        continue
                    result = DATABASE.list()
                    print("Collections in the database :")
                    print(json.dumps(result, indent=4))

                else:
                    print('Unknown database subcommand.')
                    
            elif args.command == 'collection':
                if DATABASE is None:
                    print("No database initialized. Please initialize a database first.")
                    continue

                if args.collection_command == 'create':
                    collection_name = args.collection_name
                    DATABASE.collection(collection_name)
                    print(f"Collection '{collection_name}' created.")

                elif args.collection_command == 'drop':
                    collection_name = args.collection_name
                    result = DATABASE.drop_collection(collection_name)
                    print(f"Collection '{collection_name}' dropped.")

                elif args.collection_command == 'set_schema':
                    collection_name = args.collection_name
                    safe_globals = {"__builtins__": {}, "str": str, "int": int, "bool": bool, "float": float, "datetime": datetime}
                    schema = eval(args.schema, safe_globals)
                    DATABASE.set_schema(collection_name, schema)
                    print(f"Schema for collection '{collection_name}' set.")

                elif args.collection_command == 'get_schema':
                    collection_name = args.collection_name
                    schema = DATABASE.get_schema(collection_name)
                    print(f"Schema for collection '{collection_name}':")
                    print(json.dumps(schema, indent=4, default=str))

                elif args.collection_command == 'get_data':
                    collection_name = args.collection_name
                    data = DATABASE.get_collection_data(collection_name)
                    print(f"Data for collection '{collection_name}':")
                    print(json.dumps(data, indent=4))
                    
                else:
                    print('Unknown collection subcommand.')
                    
            elif args.command == 'document':
                if DATABASE is None:
                    print("No database initialized. Please initialize a database first.")
                    continue

                if args.document_command == 'add':
                    collection_name = args.collection_name
                    document = eval(args.document)
                    DATABASE.add(collection_name, document)
                    print(f"Document added to collection '{collection_name}'.")

                elif args.document_command == 'add_many':
                    collection_name = args.collection_name
                    documents = eval(args.documents)
                    DATABASE.add_many(collection_name, documents)
                    print(f"{len(documents)} documents added to collection '{collection_name}'.")

                elif args.document_command == 'update':
                    collection_name = args.collection_name
                    update = eval(args.update)
                    query = eval(args.query)
                    limit = args.limit
                    updated_docs = DATABASE.update(collection_name, update, query, limit)
                    print(f"Updated {len(updated_docs)} documents in collection '{collection_name}'.")

                elif args.document_command == 'delete':
                    collection_name = args.collection_name
                    query = eval(args.query)
                    limit = args.limit
                    deleted_docs = DATABASE.delete(collection_name, query, limit)
                    print(f"Deleted {len(deleted_docs)} documents from collection '{collection_name}'.")
                
                else:
                    print('Unknown document subcommand.')
                    
            elif args.command == 'find':
                if DATABASE is None:
                    print("No database initialized. Please initialize a database first.")
                    continue
                
                collection_name = args.collection_name
                query = eval(args.query) if args.query else {}
                limit = args.limit
                skip = args.skip
                sort = args.sort
                order = args.order

                results = DATABASE.find(collection_name, query, limit, skip, sort, order)
                
                if not results:
                    print("No matching documents found.")
                    continue

                table = BeautifulTable()
                table.set_style(BeautifulTable.STYLE_BOX_DOUBLED)
                table.columns.header = ["_id"] + [key for key in results[0] if key != "_id"]

                for doc in results:
                    table.rows.append([doc["_id"]] + [doc[key] for key in doc if key != "_id"])

                print(table)
                
            elif args.command == 'backup':
                if DATABASE is None:
                    print("No database initialized. Please initialize a database first.")
                    continue
                
                backup_file = args.backup_file
                DATABASE.backup_db(backup_file)
                print(f"Database backed up to '{backup_file}'.")

            elif args.command == 'restore':
                if DATABASE is None:
                    print("No database initialized. Please initialize a database first.")
                    continue

                backup_file = args.backup_file
                DATABASE.restore_db(backup_file)
                print(f"Database restored from '{backup_file}'.")

            else:
                print('Unknown Command.')

        except SystemExit:
            pass
        except Exception as e:
            print(f"Error: {e.message}")

if __name__ == '__main__':
    main()
