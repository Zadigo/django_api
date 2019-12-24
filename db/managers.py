from django_api.db.functions import Functions
from itertools import dropwhile, filterfalse
from django_api.db.queryset import QuerySet

class Manager(Functions):
    """A class that regroups all the base functionnalities for
    interracting with the database
    """
    def __init__(self, data=None):
        self.db_data = data

    def insert(self, **kwargs):
        pass
    
    def _all(self):
        return self.db_data

    def include(self, *fields):
        pass

    def exclude(self, *fields):
        """Get certain fields by excluding those that you do need"""
        data = {}
        values = []
        for item in self.values():
            for key, value in item.items():
                for field in fields:
                    if key != field:
                        data[key] = value
            values.append(data)
        return values


    def get(self, **query):
        """Get a single item from the database
        """
        if 'id' in query:
            # If the user passes a single numeric
            # item, then we can return on item
            if not isinstance(query['id'], list):
                return self.get_by_id(int(query['id']))
            # Otherwise, if we get a list or a tuple,
            # it means we need to return multiple items
        return self.iterator(**query)

    def get_or_create(self, **kwargs):
        available_fields = self.available_keys()
        base_structure = dict()
        base_structure.update({available_field for available_field in available_fields})

    def filter(self, **query):
        """Retrieve data based on a list of filters"""
        return QuerySet(self.iterator(**query))

    def update(self, **kwargs):
        pass

    def update_or_create(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass

    def select_related(self, *keys):
        pass

    def values(self):
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
