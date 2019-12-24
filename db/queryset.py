from itertools import dropwhile, takewhile, filterfalse

class QuerySet:
    def __init__(self, data):
        self.data = data

    def values(self):
        """Return the items of the database as an array of dictionnaries"""
        # If the data we receive is already a list,
        # then we can just return the data without
        # any iteration whatsoever
        if isinstance(self.data, list):
            return self.data
        if isinstance(self.data, dict):
            return self.data
        return [data for data in self.data]

    def limit(self, n):
        """Return a list of items"""
        return self.values()[:n]

    def count(self):
        """Return the number of items in the database"""
        return len(self.values())

    def last(self):
        """Return the last item of the queryset"""
        return self.values()[-1]

    def first(self):
        """Return the first item of the queryset"""
        return self.values()[0]
