from django_api.db.database import Database
from django_api.db.queryset import QuerySet
from django_api.db.operators import OR, AND, Where, Annotate, F

PATH = 'C:\\Users\\Pende\\Documents\\myapps\\django_api\\db\\database.json'
database = Database(path_or_url=PATH)

# GET
# qs = database.manager.get(surname='Jenner')
# database.manager.get(surname__name='Jenner')
# qs = database.manager.get(location__country='USA')
# database.manager.get(location='USA')
# qs = database.manager.get_or_create(surname='Jenner')
# qs = database.manager.get(id=2)
# qs = database.manager.get(id=8)
# qs = database.manager.get(age__lt=24)
# qs = database.manager.get(age__gt=24)
# qs = database.manager.get(age__eq=22)
# qs = database.manager.get(age__ne=22)
# qs = database.manager.get(age__lte=22)
# qs = database.manager.get(age__gte=22)
# qs = database.manager.get(age=22)
# qs = database.manager.get(name__contains='Hai')
# qs = database.manager.get(name__exact='Hailey')

# FILTER
qs = database.manager.filter(surname__contains='Ken')
# qs = database.manager.exclude('name', 'surname')
# qs = database.manager.include('location')

# SPECIAL
# qs = database.manager.count()

# QUERYSET
# qs = QuerySet(database.db_data)
# e = qs.limit(2)
# e = qs.first()
# e = qs.last()

# database.create('Something', ['Celebrities'], ['name', 'surname', 'age'])

print(qs.values())
# print(e)