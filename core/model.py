from sqlalchemy import func
from core.schema import UploadRecord, session_scope
from core.utils import Utils


class SQLiteModel:

    # 查询一个record
    def get_one_record(self, name, upload_way):
        with session_scope() as s:
            record = s.query(UploadRecord).filter(
                UploadRecord.name == name,
                UploadRecord.upload_way == upload_way,
            ).first()
            return record

    # 添加一个record
    def add_one_record(self, name, fullname, upload_way):
        with session_scope() as s:
            record = s.query(UploadRecord).filter(
                UploadRecord.name == name,
                UploadRecord.upload_way == upload_way,
            ).first()
            if not record:
                s.add(UploadRecord(
                    name=name,
                    fullname=fullname,
                    upload_way=upload_way,
                    created_at=Utils.now(return_datetime=True)
                ))

    @staticmethod
    def get_fullname_by_name(name, upload_way):
        with session_scope() as s:
            record = s.query(UploadRecord.fullname).filter(
                UploadRecord.name == name,
                UploadRecord.upload_way == upload_way,
            ).first()
            return record
