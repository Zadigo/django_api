from db.functions import Functions

class Operators(Functions):
    def __init__(self, **kwargs):
        self.query = kwargs

    def __repr__(self):
        return f'{self.__class__.__name__}({self.query})'

class Where(Operators):
    def __init__(self, if_condition=None, then_condition=None, else_condition=None, **kwargs):
        super().__init__(**kwargs)

    def decompose(self):
        pass

class Or(Operators):
    pass
