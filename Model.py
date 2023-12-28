from sqlalchemy import Integer, ForeignKey, Boolean, Text, create_engine
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship, Session

Base = declarative_base()

engine = create_engine("sqlite:///database.db", echo=False)
session = Session(engine)


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
    name: Mapped[str] = mapped_column(Text(), nullable=False, unique=True)
    parts = relationship("Part", back_populates="part_type")


class Project(Base):
    __tablename__ = "project"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text(), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text(), nullable=True)
    link: Mapped[str] = mapped_column(Text(), nullable=False)
    archived: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    parts = relationship("Part", back_populates="part_use")


Base.metadata.create_all(engine)

if len(session.query(Part).all()) == 0:
    arduino_type = Type(name="arduino")
    uno = Part(place="here")
    arduino_type.parts = [uno]
    session.add(arduino_type)
    session.add(uno)
    p = Project(name="test_p", link="ttt")
    p.parts = [uno]
    session.add(p)
