from django_api.db.database import Database

PATH = 'C:\\Users\\Pende\\Documents\\myapps\\django_api\\db\\database.json'
database = Database(path_or_url=PATH)

# print(database.db_data)

# print(database.manager.last_item_id)
# print(database.manager.auto_increment_last_id)
# print(database.manager.get(location='ITA'))
# database.manager.get_or_create(surname='Jenner')


# database.manager.get(surname='Jenner')
# database.manager.get(surname__name='Jenner')
# print(database.manager.get(location__country='USA'))
# print(database.manager.get(location='USA'))
# print(database.manager.count())
print(database.manager.get(id=8))