import json
from sqlalchemy import and_
from sqlalchemy.exc import NoResultFound

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
        try:
            t = session.query(Type).filter(Type.name == p_type).one()
        except NoResultFound:
            return json.dumps({"status": "error", "details": "type not found"})
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

    @staticmethod
    def get_all_types():
        q = session.query(Type).all()
        info = list()
        for numb, i in enumerate(q):
            total = len(i.parts)
            free = session.query(Part).filter(and_(Part.in_project == False, Part.part_type == i)).count()
            info.append({"name": i.name, "parts_free": f"{free}/{total}"})
        return json.dumps({"status": "ok", "types": info})

    @staticmethod
    def add_to_project(id_: int, proj_name: str):
        try:
            project = session.query(Project).filter(Project.name == proj_name).one()
        except NoResultFound:
            return json.dumps({"status": "error", "details": "project not found"})
        try:
            detail = session.query(Part).filter(Part.id == id_).one()
        except NoResultFound:
            return json.dumps({"status": "error", "details": "part not found"})
        if detail.in_project:
            return json.dumps({"status": "error", "details": "part already used"})
        if project.archived:
            return json.dumps({"status": "error", "details": "project archived"})
        project.parts.append(detail)
        detail.in_project = True
        session.commit()
        return json.dumps({"status": "ok", "details": ""})

    @staticmethod
    def get_all_projects():
        projects = session.query(Project).all()
        info = list()
        for numb, i in enumerate(projects):
            info.append({"name": i.name, "archive": f"{i.archived}"})
        return json.dumps({"status": "ok", "projects": info})

    @staticmethod
    def get_type_info(name: str):
        try:
            my_type = session.query(Type).filter(Type.name == name).one()
        except NoResultFound:
            return json.dumps({"status": "error", "details": "type not found"})
        total = len(my_type.parts)
        free = session.query(Part).filter(and_(Part.in_project == False, Part.part_type == my_type)).count()
        js = {"status": "ok", "name": name, "parts_free": f"{total}/{free}"}
        parts = []
        for i in my_type.parts:
            parts.append({"part_id": str(i.id), "free": str(not i.in_project)})
        js["parts"] = parts
        return json.dumps(js)
