from sqlalchemy import create_engine, Integer, ForeignKey
from sqlalchemy.orm import Session, declarative_base, relationship

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Text, Boolean

engine = create_engine("sqlite:///database.db", echo=False)
session = Session(engine)
Base = declarative_base()


class Part(Base):
    __tablename__ = "part"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[int] = mapped_column(Integer(), ForeignKey('type.id', ondelete='CASCADE'), )
    proj: Mapped[int] = mapped_column(Integer(), ForeignKey('project.id', ondelete='CASCADE'), default=0)
    in_project: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)
    place: Mapped[str] = mapped_column(Text(), nullable=False)
    info: Mapped[str] = mapped_column(Text(), nullable=True)
    part_type = relationship("Type", back_populates="parts")
    part_use = relationship("Project", back_populates="parts")


class Type(Base):
    __tablename__ = "type"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text(), nullable=False)
    parts = relationship("Part", back_populates="part_type")


class Project(Base):
    __tablename__ = "project"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text(), nullable=False)
    description: Mapped[str] = mapped_column(Text(), nullable=True)
    link: Mapped[str] = mapped_column(Text(), nullable=False)
    archived: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    parts = relationship("Part", back_populates="part_use")


Base.metadata.create_all(engine)

arduino_type = Type(name="arduino")
uno = Part(place="here")
arduino_type.parts = [uno]
session.add(arduino_type)
session.add(uno)
p = Project(name="test_p", link="ttt")
p.parts = [uno]
session.add(p)
'''t = session.query(Part).all()
print(t[0].part_type.name)'''
for i in session.query(Project).all():
    print(i.parts)
    print(i.parts[0].part_type.name)
session.commit()
