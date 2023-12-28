import json


class DbConnector:
    session = None

    def __init__(self):
        pass

    @staticmethod
    def set_session(session):
        DbConnector.session = session

    @staticmethod
    def add_part(p_type: str, info: str, place: str):
        if place is None or len(place) == 0:
            return json.dumps({"status": "error", "details": "place not specified"})
        from Model import Part, Type, Project
        p = Part(type=p_type, info=info, place=place)
        t = DbConnector.session.query(Type).filter(Type.name == p_type).all()
        if len(t) == 0:
            return json.dumps({"status": "error", "details": "type not found"})
        t = t[0]  # because only one can be
        t.parts.append(p)
        print(t.parts)
        DbConnector.session.commit()
        return json.dumps({"status": "ok", "details": ""})
