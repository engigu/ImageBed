from sqlalchemy import func
from core.schema import UploadRecord, session_scope
from core.utils import Utils


class SQLiteModel:

    # 查询一个record
    def get_one_record(self, name):
        with session_scope() as s:
            record = s.query(UploadRecord).filter(UploadRecord.name == name).first()
            return record

    # 添加一个record
    def add_one_record(self, name):
        with session_scope() as s:
            s.add(UploadRecord(
                name=name,
                created_at=Utils.now(return_datetime=False)
            ))
          