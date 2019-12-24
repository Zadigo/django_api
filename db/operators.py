from django_api.db.functions import Functions
import re

class Operators:
    def __init__(self, *args):
        self.args = args

    # def filters(self):
    #     return list(self.query[0].keys())

    # def values(self):
    #     return list(self.query[0].values())

    def decompose(self, *args):
        """Decompose each string into a dictionnary
        """
        for arg in args:
            query = arg.split('=')
            yield {query[0], query[1]}
    
    def __repr__(self):
        return {'name': 'Kendall', 'surname': 'Hailey'}

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return {'name': 'Kendall', 'surname': 'Hailey'}
        
class Where(Operators):
    def __init__(self, if_condition=None, then_condition=None, else_condition=None):
        first_condition = super().decompose(if_condition)
        self.query = first_condition

class OR(Operators):
    pass

class AND(Operators):
    pass

class Annotate(Operators):
    pass

class F:
    """The F class represents a field at the row the level
    """
    def __init__(self, field):
        pass