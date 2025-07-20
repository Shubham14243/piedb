import time
import json
import random
import string
import hashlib
from datetime import datetime

from .error import SchemaValidationError


class Utility:
    """Utility class for common operations in Piedb."""
    
    @staticmethod
    def generate_id(collection_name: str, length: int =12) -> str:
        """Generate an UniqueId."""
        
        timestamp = int(time.time())
        timestamp_str = format(timestamp, 'x')[:6]
        
        collection_hash = hashlib.md5(collection_name.encode()).hexdigest()[:3]
        
        random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

        return random_str + collection_hash + timestamp_str

    @staticmethod
    def _type_to_string(schema: dict) -> dict:
        """Convert schema types to string representations and validate supported types."""
    
        def validate_and_convert(d):
            type_map = {"str": str, "int": int, "float": float, "bool": bool, "dict": dict, "list": list, "datetime": datetime}
            
            if not isinstance(d, dict):
                raise SchemaValidationError("Schema must be a dictionary.")
            
            converted = {}
            for k, v in d.items():
                if isinstance(v, dict):
                    converted[k] = validate_and_convert(v)
                elif isinstance(v, type):
                    if v not in type_map.values():
                        raise SchemaValidationError(f"Unsupported type: {v}")
                    converted[k] = v.__name__
                else:
                    raise SchemaValidationError(f"Invalid schema definition for '{k}': {v}")
            return converted

        return validate_and_convert(schema)

    @staticmethod
    def _string_to_type(schema: dict) -> dict:
        """Convert string representations back to types."""
        type_map = {"str": str, "int": int, "float": float, "bool": bool, "dict": dict, "list": list, "datetime": datetime}
        return {k: type_map[v] for k, v in schema.items()}
    
    @staticmethod
    def unique_collection_name(base_name: str, db: dict) -> str:
        """Find a unique collection name by appending an incrementing number."""
        i = 1
        while f"{base_name}_{i}" in db:
            i += 1
        return f"{base_name}_{i}"
        
    @staticmethod
    def _normalize_schema(schema: dict) -> dict:
        """
        Normalize a schema dict:
        - sort keys
        - lowercase type names
        - recursively handle nested dicts
        """

        if not isinstance(schema, dict):
            return schema

        normalized = {}
        for key in sorted(schema.keys()):
            value = schema[key]
            if isinstance(value, dict):
                normalized[key] = Utility._normalize_schema(value)
            elif isinstance(value, str):
                normalized[key] = value.lower()
            else:
                normalized[key] = value
        return normalized

    
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime): 
            return obj.isoformat()
        return super().default(obj)
    