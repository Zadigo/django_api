class Functions:
    db_data = []
    special_words = ['eq', 'gt', 'gte', 'lt', 'lte', 
                        'ne', 'contains', 'icontains', 'exact', 'iexact']
    keys_dict = []
    searched_values = []
    
    def decompose(self, query):
        # Now we can seperate the keys from
        # the search values so that we have
        # two independent arrays from one another
        # query = {'name': 'Kendall', 'location__country': 'USA'}
        # query = {'location__country': 'USA'}
        for key, value in query.items():
            self.keys_dict.append(key)
            self.searched_values.append(value)

    def available_keys(self, check_key=None):
        """Returns the list of available keys that can
        be used to query the data

        Parameters
        ----------

            check_key_in: pass a string to check if something
            is present in the available keys        
        """
        if self.db_data is None:
            return []
        # We can come from the premise
        # that all the values are structured
        # the exact same manner -- in which
        # case, by taking on sample from the
        # data that we want to query, we can
        # get the general keys' structure 
        # of all the rest of the data
        keys = [key for key in self.db_data.keys()]

        if check_key:
            if check_key in keys:
                return True
            else:
                return False

        # Now get the available keys
        # from the sample dict
        return keys

    def right_hand_filter(self, f, sub_dict):
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
            if key not in self.special_words:
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
                    if key not in self.special_words:
                        raise
        # If everything went well,
        # we should have got the
        # value that we were looking for
        return sub_dict

    def comparator(self, a, b, special_word='exact'):
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

    def iterator(self, query=None):
        """This definition iterates over each dict in the data
        that we wish to filter and then operates somekind of
        logic in order to extract the elements
        """
        self.decompose(query)

        comparator_results = []
        filtered_items = []
        number_of_values_to_search = len(self.searched_values)
        position = 0
        # This section iterates over both
        # arrays in order to filter the data
        for item in self.db_data:
            for key in self.keys_dict:
                searched_value = self.searched_values[position]
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
                    with_underscore = self.right_hand_filter(key, item)

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
                comparator_results.append(self.comparator(g, searched_value, special_word='exact'))
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

class Operators:
    def __init__(self, **kwargs):
        self.query = kwargs

    def __repr__(self):
        return f'{self.__class__.__name__}({self.query})'

class Where(Operators):
    def __init__(self, condition=None, **kwargs):
        super().__init__(**kwargs)

class Or(Operators):
    pass
