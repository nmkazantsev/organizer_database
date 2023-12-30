from DbFunctions import DbConnector

print(DbConnector.create_device(name="arduino", total=3, place="here"))
print(DbConnector.create_device(name="esp", total=3, place="here"))
print(DbConnector.delete_device(2))
print(DbConnector.edit_device(3, name="esp8266"))
print(DbConnector.create_project("second", description="2 project", link="http://amperka.ru"))
print(DbConnector.edit_project(2, link="http://amperka.ru2", archived=not True))
print(DbConnector.add_detail_to_project(1, 1, 1))
print(DbConnector.edit_details(1, 1, 4))
print(DbConnector.edit_details(1, 1, 0))
