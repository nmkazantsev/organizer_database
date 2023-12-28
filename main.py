from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from Model import create_db, Part, Type, Project
from DbFunctions import DbConnector

engine = create_engine("sqlite:///database.db", echo=False)
session = Session(engine)

create_db(engine)

if len(session.query(Part).all()) == 0:
    arduino_type = Type(name="arduino")
    uno = Part(place="here")
    arduino_type.parts = [uno]
    session.add(arduino_type)
    session.add(uno)
    p = Project(name="test_p", link="ttt")
    p.parts = [uno]
    session.add(p)

DbConnector.set_engine(engine)
print(DbConnector.add_part("esp", "second", "there"))
print(DbConnector.add_type("esp"))
print(DbConnector.add_proj(name="second", link="http"))
