from sqlalchemy import Integer, ForeignKey, Boolean, Text, create_engine, Table, Column, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship, Session

Base = declarative_base()

engine = create_engine("sqlite:///database.db", echo=False)
session = Session(engine)


class Association(Base):
    __tablename__ = "association_table"
    project_id = Column(ForeignKey("project_table.id"), primary_key=True)
    device_id = Column(ForeignKey("device_table.id"), primary_key=True)
    amount = Column(Integer)
    device = relationship("Device", back_populates="projects")
    project = relationship("Project", back_populates="devices")


class Project(Base):
    __tablename__ = "project_table"
    id = Column(Integer, primary_key=True)
    devices = relationship("Association", back_populates="project")
    name = Column(Text(), unique=True, nullable=False)
    description = Column(Text())
    link = Column(Text())
    archived = Column(Boolean(), default=False)


class Device(Base):
    __tablename__ = "device_table"
    id = Column(Integer, primary_key=True)
    projects = relationship("Association", back_populates="device")
    name = Column(Text(), unique=True, nullable=False)
    place = Column(Text(), nullable=False)
    total = Column(Integer(), default=0)
    used = Column(Integer(), default=0)


Base.metadata.create_all(engine)

if len(session.query(Device).all()) == 0:
    arduino = Device(name="arduino")
    m = Project(name="new")
    a = Association(amount=2)
    a.device = arduino
    m.devices = [a]
    session.add(m)
    session.add(arduino)
    print(session.query(Device).all()[0].projects[0].device.name)
    session.commit()
