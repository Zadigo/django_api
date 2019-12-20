import json
import secrets
import datetime
from db.functions import Functions

PATH = 'C:\\Users\\Pende\\Documents\\myapps\\django_api\\db\\database.json'

# Other functions
def database_cache(func):
    def load_database(self, path_or_url=None, **kwargs):
        """Opens the database and returns a cached version
        of the data that it contains
        """
        cached_data = func(self)
        return cached_data
    return load_database

class Manager(Functions):
    def __init__(self, data=None):
        self.db_data = data

    def insert(self, **kwargs):
        pass

    def get(self, **kwargs):
        return self.iterator(**kwargs)

    def get_or_create(self, **kwargs):
        pass

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
        return [data for data in test_data.values()]

    @classmethod
    def limit(cls, n, **kwargs):
        return cls.filter(**kwargs)[:n]

    def first(self):
        return self.values()[0]

    def last(self):
        return self.values()[-1]

    def count(self):
        return len(self.values())

    @classmethod
    def as_manager(cls, data=None):
        """Instantiates the manager once again and
        returns the class
        """
        return cls(data=data)

class QuerySet(Functions):
    pass

class Database(QuerySet):
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
        return datetime.datetime.now().timestamp()

    @staticmethod
    def calculate_version(n):
        return n + 1

    def clean(self, **kwargs):
        """This definition is called just before data is committed (or written)
        to the database in order to prevent corruption.
        """
        pass
    
class Models(Database):
    """Models are a way of structuring the logic of your database
    efficiently using class methods.

    Description
    -----------

        class FashionModels(Models):
            pass
    """
    pass



# Testing
# database = Database()
# database.breakdown(name='Kendall')
# database.breakdown(name='Kendall', location__contains='Kendall', name__age__eq=15)


# def age_validator(n):
#     if n == 22:
#         raise Exception()
#     return n

# class Fashion(Models):
#     name = CharField(max_length=34, verbose_name='Name')
#     age = PositiveIntegerField(minimum=18, maximum=34)
#     description = TextField(54)
#     created_on = DateField()

# mymodel = Fashion()
# print(mymodel.create_database())

# Functions
# functions = Functions()
# functions.breakdown(name='Kendall')


from itertools import dropwhile, filterfalse, takewhile

database = Database(path_or_url=PATH)
test_data = database.db_data

special_words = ['eq', 'gt', 'gte', 'lt', 'lte', 
                    'ne', 'contains', 'icontains']
# An array containing all
# the searched keys in a query
keys_dict = []
searched_values = []

# Now we can seperate the keys from
# the search values so that we have
# two independent arrays from one another
# query = {'name': 'Kendall', 'location__country': 'USA'}
# query = {'location__country': 'USA'}
query = {'age__eq': 26}
for key, value in query.items():
    keys_dict.append(key)
    searched_values.append(value)

# Decompose the data into an
# array containing the dicts
# without their primary keys
# in order to faciliate iteration
data = [data for data in test_data.values()]

def comparator(a, b, special_word='exact'):
    """A definition used to compare two given values
    and returns True or False.

    Parameters:

        a: the reference value to compare

        b: the value the user wants to compare to a

        special_word: the filter word to use to make the comparision
    """
    if special_word == 'exact' or special_word == 'eq':
        return a == b

    if special_word == 'gt':
        return a > b

    if special_word == 'gte':
        return a >= b

    if special_word == 'lt':
        return a < b

    if special_word == 'lte':
        return a <= b

    if special_word == 'contains':
        return a in b

def right_hand_filter(f, sub_dict):
    """A special function that takes the extended
    queries in order to transform them into a logic
    that can filter the data from the database

    Description
    -----------

        {location: {country: USA}}

        Suppose we have 'location__country' as query to
        get USA in the dict above. In which case, the definition
        will split the paramaters to get the specific value.

    Parameters
    ----------

        f: a filter such as something__a or something__a__b

        sub_dict: a subdictionnary that we want to filter
    """
    splitted_values = f.split('__', 5)
    number_of_keys = len(splitted_values)

    # We iterate over each keyword
    # using the index. At each iteration,
    # we get +1 depth into the dict we
    # are trying to filter
    for i in range(0, number_of_keys):
        key = splitted_values[i]
        if key not in special_words:
            # We know that it is a 
            # dictionnary key
            try:
                # If the subdict is a dict or is still
                # a dict then we can keep going
                # +1 in depth
                if isinstance(sub_dict, dict):
                    sub_dict = sub_dict[key]
                else:
                    # Otherwise, there's nothing to
                    # query anymore and we can raise an
                    # error since the additional depth
                    # does not exist
                    raise KeyError()
            except KeyError:
                # If the key is not present,
                # we can raise an error here
                if key not in special_words:
                    raise
    # If everything went well,
    # we should have got the
    # value that we were looking for
    return sub_dict

def iterator():
    """This definition iterates over each dict in the data
    that we wish to filter and then operates somekind of
    logic in order to extract the elements
    """
    comparator_results = []
    filtered_items = []
    number_of_values_to_search = len(searched_values)
    position = 0
    # This section iterates over both
    # arrays in order to filter the data
    for item in data:
        for key in keys_dict:
            searched_value = searched_values[position]
            try:
                no_underscore = item[key]
                # There are cases where the user might
                # query a specific section of the dict
                # that will return a dict instead of a
                # value. In which case, we need to deal
                # with that by informing him that the
                # result is a dictionnary that needs to
                # be queried again or not (?)

                # Another solution is to return all the
                # subdictionnaries with that keyword
                if isinstance(no_underscore, dict):
                    filtered_items.append(item[key])
            except KeyError:
                no_underscore = None
                # If the key contains a double
                # underscore we need to separate
                # the key from special keyword
                with_underscore = right_hand_filter(key, item)

            # If we have a match,
            # we can return the item
            # if e == searched_value:
            #     yield item
            g = no_underscore or with_underscore
            # We have to refilter the item that we
            # just got using this time the other filter.
            # This is useful for cases where we have
            # multiple filters -- for that, we gather
            # the comparators results and then perform
            # an all() on the results
            comparator_results.append(comparator(g, searched_value, special_word='exact'))
            position = position + 1
            # In order for the cursor to always iterate
            # between the 0 and the max amount of values
            # that the user wants to search, we have to
            # reset it
            if position >= number_of_values_to_search:
                position = 0

        if all(comparator_results):
            filtered_items.append(item)
    return filtered_items

# print(iterator())
# print(right_hand_filter('location__address__number', {'location': {'country': 'USA', 'city': 'Florida', 'address': {'number': 1}}}))
# print(comparator('Paris', 'Kendall Jenner', special_word='contains'))
# print(iterator())
# print(iterator())
# print(Models().available_keys())
