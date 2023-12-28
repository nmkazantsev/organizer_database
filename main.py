from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Text

engine = create_engine("sqlite:///database.db", echo=True)
session = Session(engine)
Base = declarative_base()


class Part(Base):
    __tablename__ = "part"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(Text())


Base.metadata.create_all(engine)
