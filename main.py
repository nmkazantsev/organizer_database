from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from Model import Part, Type, Project
from DbFunctions import DbConnector

print(DbConnector.add_part("esp", "second", "there"))
print(DbConnector.add_type("esp"))
print(DbConnector.add_proj(name="second", link="http"))
print(DbConnector.get_all_types())
