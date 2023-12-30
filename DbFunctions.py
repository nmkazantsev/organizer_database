import json
from sqlalchemy import and_
from sqlalchemy.exc import NoResultFound, IntegrityError
from Model import Device, session


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
