class DatabaseError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class SchemaError(DatabaseError):
    pass

class FieldError(DatabaseError):
    pass

class ValidatorError(DatabaseError):
    pass
