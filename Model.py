from sqlalchemy import Integer, ForeignKey, Boolean, Text
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

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
    name: Mapped[str] = mapped_column(Text(), nullable=False, unique=True)
    parts = relationship("Part", back_populates="part_type")


class Project(Base):
    __tablename__ = "project"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text(), nullable=False)
    description: Mapped[str] = mapped_column(Text(), nullable=True)
    link: Mapped[str] = mapped_column(Text(), nullable=False)
    archived: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    parts = relationship("Part", back_populates="part_use")


def create_db(engine):
    Base.metadata.create_all(engine)
