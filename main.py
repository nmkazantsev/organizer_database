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
    in_project: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    place: Mapped[str] = mapped_column(Text(), nullable=False)
    info: Mapped[str] = mapped_column(Text(), nullable=True)
    part_type = relationship("Type", back_populates="parts")


class Type(Base):
    __tablename__ = "type"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text(), nullable=False)
    parts = relationship("Part", back_populates="part_type")


Base.metadata.create_all(engine)

'''typ = Type(name="arduino")
part = Part(in_project=False, place="here")
typ.parts = [part]
session.add(typ)
session.add(part)'''
'''t = session.query(Part).all()
print(t[0].part_type.name)'''
session.commit()
