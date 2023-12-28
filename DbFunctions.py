import json

from sqlalchemy.orm import Session

from Model import Part, Type, Project


class DbConnector:
    session = None

    def __init__(self):
        pass

    @staticmethod
    def set_engine(engine):
        DbConnector.session = Session(engine)

    @staticmethod
    def add_part(p_type: str, info: str, place: str):
        if place is None or len(place) == 0:
            return json.dumps({"status": "error", "details": "place not specified"})
        p = Part(type=p_type, info=info, place=place)
        t = DbConnector.session.query(Type).filter(Type.name == p_type).all()
        if len(t) == 0:
            return json.dumps({"status": "error", "details": "type not found"})
        t = t[0]  # because only one can be
        t.parts.append(p)
        print(t.parts)
        DbConnector.session.commit()
        return json.dumps({"status": "ok", "details": ""})

    @staticmethod
    def add_type(name: str):
        t = Type(name=name)
        DbConnector.session.add(t)
        DbConnector.session.commit()
        return json.dumps({"status": "ok", "details": ""})

    @staticmethod
    def add_proj(name: str, link: str, description: str = None):
        p = Project(name=name, description=description, link=link)
        DbConnector.session.add(p)
        DbConnector.session.commit()
        return json.dumps({"status": "ok", "details": ""})
