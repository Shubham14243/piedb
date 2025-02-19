import json
import random
import string
import time
import hashlib
from datetime import datetime


class Utility:
    
    @staticmethod
    def generate_id(collection_name, length=12):
        """Generate an UniqueId."""
        
        timestamp = int(time.time())
        timestamp_str = format(timestamp, 'x')[:6]
        
        collection_hash = hashlib.md5(collection_name.encode()).hexdigest()[:3]
        
        random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        
        return timestamp_str + collection_hash + random_part

    @staticmethod
    def _type_to_string(schema):
        """Convert schema types to string representations."""
        return {k: v.__name__ for k, v in schema.items()}

    @staticmethod
    def _string_to_type(schema):
        """Convert string representations back to types."""
        type_map = {"str": str, "int": int, "float": float, "bool": bool, "dict": dict, "list": list, "datetime": datetime}
        return {k: type_map[v] for k, v in schema.items()}
    
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime): 
            return obj.isoformat()
        return super().default(obj)