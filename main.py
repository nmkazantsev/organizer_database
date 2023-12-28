from DbFunctions import DbConnector

# print(DbConnector.add_part("esp", "second", "there"))
print(DbConnector.add_type("esp"))
print(DbConnector.add_proj(name="second", link="http"))
print(DbConnector.add_to_project(5, "second"))
print(DbConnector.add_to_project(2, "second"))
print(DbConnector.add_to_project(1, "second"))
print(DbConnector.get_all_types())
print(DbConnector.get_all_projects())
print(DbConnector.get_type_info("esp"))
print(DbConnector.get_part_info(1))
