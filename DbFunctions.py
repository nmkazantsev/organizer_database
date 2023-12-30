import json
from sqlalchemy import and_
from sqlalchemy.exc import NoResultFound, IntegrityError
from Model import Device, session, Project, Association


def ok(details=None):
    return json.dumps({"status": "ok", "details": details})


def error(details):
    return json.dumps({"status": "error", "details": details})


class DbConnector:
    session = None

    def __init__(self):
        pass

    @staticmethod
    def create_device(name: str, place: str, total: int, info: str = None, used: int = 0):
        try:
            d = Device(name=name, place=place, total=total, info=info, used=used)
            session.add(d)
            session.commit()
        except IntegrityError:
            session.rollback()
            return error("device exists")
        return ok()

    @staticmethod
    def delete_device(id_: int):
        try:
            d = session.query(Device).filter(Device.id == id_).one()
        except NoResultFound:
            return error("device does not exists")
        if len(d.projects) != 0:
            return error("device used in project")
        session.query(Device).filter(Device.id == id_).delete()
        session.commit()
        return ok()

    @staticmethod
    def edit_device(id_: int, name: str = None, place: str = None, info: str = None, total: int = None,
                    used: int = None):
        try:
            d = session.query(Device).filter(Device.id == id_).one()
        except NoResultFound:
            return error("device does not exists")
        if name is not None:
            d.name = name
        if place is not None:
            d.place = place
        if info is not None:
            d.info = info
        if total is not None:
            d.total = total
        if used is not None:
            d.used = used
        session.commit()
        return ok()

    @staticmethod
    def create_project(name: str, description: str = None, link: str = None):
        try:
            d = Project(name=name, description=description, link=link)
            session.add(d)
            session.commit()
        except IntegrityError:
            session.rollback()
            return error("project exists")
        return ok()

    @staticmethod
    def delete_project(id_: int):
        try:
            p = session.query(Project).filter(Project.id == id_).one()
        except NoResultFound:
            return error("project does not exists")
        session.query(Project).filter(Project.id == id_).delete()
        session.commit()
        return ok()

    @staticmethod
    def edit_project(id_: int, name: str = None, description: str = None, archived: bool = None, link: str = None):
        try:
            p = session.query(Project).filter(Project.id == id_).one()
        except NoResultFound:
            return error("project does not exists")
        if name is not None:
            p.name = name
        if link is not None:
            p.link = link
        if description is not None:
            p.description = description
        if archived is not None:
            p.archived = archived
            for assoc in p.devices:
                if archived:
                    assoc.device.used -= assoc.amount
                else:
                    assoc.device.used += assoc.amount
        session.commit()
        return ok()

    @staticmethod
    def edit_details(proj_id: int, device_id: int, new_amount: int):
        try:
            p = session.query(Project).filter(Project.id == proj_id).one()
        except NoResultFound:
            return error("project does not exists")
        try:
            d = session.query(Device).filter(Device.id == device_id).one()
        except NoResultFound:
            return error("device does not exists")
        if new_amount > 0:
            assoc = session.query(Association).filter(
                and_(Association.device_id == device_id, Association.project_id == proj_id)).one()
            assoc.amount = new_amount
        elif new_amount < 0:
            return error("amount < 0")
        else:
            session.query(Association).filter(
                and_(Association.device_id == device_id, Association.project_id == proj_id)).delete(
                synchronize_session='fetch')

        session.commit()
        return ok()

    @staticmethod
    def add_detail_to_project(detail_id: int, project_id: int, amount: int = 1):
        try:
            p = session.query(Project).filter(Project.id == project_id).one()
        except NoResultFound:
            return error("project does not exists")
        try:
            d = session.query(Device).filter(Device.id == detail_id).one()
        except NoResultFound:
            return error("device does not exists")
        if d in [i.device for i in p.devices]:
            return error("device already added")
        a = Association(amount=amount)
        a.device = d
        p.devices.append(a)
        session.commit()
        return ok()
