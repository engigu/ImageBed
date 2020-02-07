from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, VARCHAR, DATETIME, func, or_, and_, distinct, TIMESTAMP, text, String
from contextlib import contextmanager

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import Config

Base = declarative_base()


def init_sqlite():
    path = Config.SQLITE_URI.split('sqlite:///')[-1]
    db_path = '/'.join(path.split('/')[:-1])
    if not os.path.exists(db_path):
        os.makedirs(db_path)
    Base.metadata.create_all(engine)


class UploadRecord(Base):
    __tablename__ = "upload_record"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), server_default=text("''"))
    created_at = Column(TIMESTAMP,  server_default=text("CURRENT_TIMESTAMP"))


engine = create_engine(Config.SQLITE_URI, echo=False)
session = sessionmaker(bind=engine)
SessionType = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))


def GetSession():
    return SessionType()


@contextmanager
def session_scope():
    session = GetSession()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    init_sqlite()
