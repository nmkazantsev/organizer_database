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
            return error("device exists")
        session.commit()
        return ok()
