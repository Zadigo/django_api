import json
import secrets
import datetime
from django_api.db.functions import Functions
from django_api.db.errors import SchemaError
from django_api.db.decorators import database_cache

PATH = 'C:\\Users\\Pende\\Documents\\myapps\\django_api\\db\\database.json'

class QuerySet(Functions):
    def __init__(self, data):
        pass

    def values(self):
        pass

    def limit(self, n):
        pass

    def count(self):
        """Return the number of items in the database"""
        return len(self.values())

    def last(self):
        """Return the last item of the queryset"""
        pass

    def first(self):
        """Return the first item of the queryset"""
        pass

class Manager(Functions):
    def __init__(self, data=None):
        self.db_data = data

    def insert(self, **kwargs):
        pass
    
    def _all(self):
        return self.db_data

    def include(self, **query):
        pass

    def exclude(self, **query):
        pass

    def get(self, **query):
        """Get a single item from the database
        """
        if 'id' in query:
            return self.get_by_id(int(query['id']))
        return self.iterator(**query)

    def get_or_create(self, **kwargs):
        available_fields = self.available_keys()
        base_structure = dict()
        base_structure.update({available_field for available_field in available_fields})

    def filter(self, **kwargs):
        pass

    def update(self, **kwargs):
        pass

    def update_or_create(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass

    def select_related(self, *keys):
        pass

    def values(self, *only):
        """Return the items of the database as an array of dictionnaries"""
        return [data for data in self.db_data.values()]

    @classmethod
    def limit(cls, n, **kwargs):
        return cls.filter(**kwargs)[:n]

    def first(self):
        """Return the first value of the database"""
        return self.values()[0]

    def last(self):
        """Return the last value of the database"""
        return self.values()[-1]

    def count(self):
        """Return the number of items in the database"""
        return len(self.values())

    @classmethod
    def as_manager(cls, data=None):
        """Instantiates the manager once again and
        returns the class
        """
        return cls(data=data)

class Database(Functions):
    """You can either create a database directly by using this class
    or by subclassing the Models class.

    Description
    -----------

        If you wish to create a database directly using this class,
        here's the path to follow:

            database = Database(path_or_url='', fields=[], field_types=[])

            path_or_url: is the path or the url of the schema/json that you wish to use

            fields: are the fields that you want to create if the database does not exist

            types: are the types of each fields

            This process can be facilitated by using the Fields classes such as
            IntegerField, CharField etc.
    """
    def __init__(self, **kwargs):
        if 'path_or_url' in kwargs:
            # We have to load the database
            db_data = self.load_database(kwargs['path_or_url'])['data']
            self.db_data = db_data
            self.manager = Manager(data=db_data)

    def create_database(self, name, fields, **kwargs):
        """A definition that can create a database outside of
        of a class based structure.

        Description
        -----------

            Suppose we want to create a new database and return the
            handle (cursor) of the latter. We can do so by using:

        Parameters
        ----------

            Fields: they can be either string values or Field classes that
            we be converted accordingly for the database
        """
        # Then we can migrate the database
        self.migrate(model=name)
        pass

    def migrate(self, **kwargs):
        """Creates a new version of the database by changing the
        modified_on and increasing the version of the schema
        """
        # current_data = self.load_database()
        # Increase the version of the database
        # current_data['$version'] = self.calculate_version(current_data['$version'])
        # return self.save(data=current_data)
        pass

    @classmethod
    def save(cls, data=None, **kwargs):
        """A definition that commits changes to the database
        by writting objects into it
        """
        # If data is None, then
        # just return the cached_version
        # of the database to the user
        if data is None:
            return ''

        # If data is passed but is not a dict,
        # then directly raise an exception here
        if data and not isinstance(data, dict):
            raise Exception()
        else:
            # cls.clean(data=data)

            # Otherwise we can open the database in order
            # to commit the new changes
            with open(PATH, 'w', encoding='utf-8') as f:
                data['$modified_on'] = cls.set_date()
                json.dump(data , f, indent=4, sort_keys=True)
            return cls

    @database_cache
    def load_database(self):
        """A simple function that opens the local database
        to retrieve all the data that it contains
        """
        with open(PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return self.check_schema(data)

    def refresh_from_database(self):
        pass

    def check_schema(self, data):
        # The database should have a unique
        # schema identifier for keeping track
        # of the database versions
        if '$id' not in data:
            raise SchemaError('We could not find the required key $id in the schema of your database')
        else:
            # Here we create a valid identifier for the
            # the databaase if it is none or blank
            if data['$id'] is None or data['$id'] == '':
                data['$id'] = secrets.token_hex(nbytes=25)

        # Require a created_on date so that we
        # can also keep track of the version of
        # the database
        if '$created_on' not in data:
            data['$created_on'] = self.set_date()
        else:
            if data['$created_on'] == None or data['$created_on'] == '':
                data['$created_on'] = self.set_date()

        if '$version' not in data:
            data['$version'] = 0
        else:
            if data['$version'] == None or data['$version'] == '':
                data['$created_on'] = 0
        return data

    @staticmethod
    def set_date():
        """Get the current date as a timestamp"""
        return datetime.datetime.now().timestamp()

    @staticmethod
    def calculate_version(n):
        """Bump the current database version by one"""
        return n + 1

    def clean(self, **kwargs):
        """This definition is called just before data is committed (or written)
        to the database in order to prevent corruption.
        """
        pass
