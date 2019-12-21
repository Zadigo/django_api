def database_cache(func):
    def load_database(self, path_or_url=None, **kwargs):
        """Opens the database and returns a cached version
        of the data that it contains
        """
        cached_data = func(self)
        return cached_data
    return load_database