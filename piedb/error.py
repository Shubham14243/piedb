class CollectionNotFoundError(Exception):
    """Raised when a requested collection does not exist."""
    
    def __init__(self, collection, message="Collection not found in DB"):
        self.collection = collection
        self.message = f'{message} : {collection}'
        super().__init__(self.message)


class SchemaValidationError(Exception):
    """Raised when a document does not conform to the collection's schema."""
    
    def __init__(self, custom_message, message="Schema validation failed for Document"):
        self.custom_message = custom_message
        self.message = f'{message} : {custom_message}'
        super().__init__(self.message)


class DocumentValidationError(Exception):
    """Raised when a document has invalid fields or missing data."""
    
    def __init__(self,custom_message, message="Data validation failed for Document"):
        self.custom_message = custom_message
        self.message = f'{message} : {custom_message}'
        super().__init__(self.message)


class ReservedKeyError(Exception):
    """Raised when no document matches the query."""
    
    def __init__(self, message="are reserved keys."):
        self.keys = "_schemas and _counts"
        self.message = f"{self.keys} {message}"
        super().__init__(self.message)

