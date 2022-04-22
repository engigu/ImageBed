from config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, VARCHAR, DATETIME, func, or_, and_, distinct, TIMESTAMP, text, String
from contextlib import contextmanager

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

Base = declarative_base()


class UploadRecord(Base):
    __tablename__ = "upload_record"
    id = Column(Integer, primary_key=True, autoincrement=True)
    upload_way = Column(String(64), server_default=text("''"), comment='上传途径')
    name = Column(String(64), server_default=text("''"), comment='文件名(文件的md5值+后缀，确保唯一)')
    fullname = Column(String(10240), server_default=text("''"), comment='包含文件夹的全路径文件名')
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='创建日期')


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


def init_sqlite():
    # 谨慎调用，会直接删除已有db文件
    path = Config.SQLITE_URI.split('sqlite:///')[-1]
    db_path = '/'.join(path.split('/')[:-1])
    if os.path.exists(path):
        # os.remove(path)
        pass
    else:
        if not os.path.exists(db_path):
            os.makedirs(db_path)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    # init_sqlite()
    pass
