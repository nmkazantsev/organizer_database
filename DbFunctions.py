import json

from Model import Part, Type, Project, session


class DbConnector:
    session = None

    def __init__(self):
        pass

    @staticmethod
    def add_part(p_type: str, info: str, place: str):
        if place is None or len(place) == 0:
            return json.dumps({"status": "error", "details": "place not specified"})
        p = Part(type=p_type, info=info, place=place)
        t = session.query(Type).filter(Type.name == p_type).all()
        if len(t) == 0:
            return json.dumps({"status": "error", "details": "type not found"})
        t = t[0]  # because only one can be
        t.parts.append(p)
        session.commit()
        return json.dumps({"status": "ok", "details": ""})

    @staticmethod
    def add_type(name: str):
        q = session.query(Type).filter(Type.name == name).all()
        if len(q) > 0:
            return json.dumps({"status": "error", "details": "type exists"})
        t = Type(name=name)
        session.add(t)
        session.commit()
        return json.dumps({"status": "ok", "details": ""})

    @staticmethod
    def add_proj(name: str, link: str, description: str = None):
        q = session.query(Project).filter(Project.name == name).all()
        if len(q) > 0:
            return json.dumps({"status": "error", "details": "project exists"})
        p = Project(name=name, description=description, link=link)
        session.add(p)
        session.commit()
        return json.dumps({"status": "ok", "details": ""})
