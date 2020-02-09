import datetime
import os

from sqlalchemy import TIMESTAMP


class Utils:

    @staticmethod
    def now(return_datetime=False):
        if not return_datetime:
            return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return datetime.datetime.now()

    @staticmethod
    def run_in_docker():
        return bool(os.environ.get('RUN_IN_DOCKER'))

    @staticmethod
    def row2dict(row):
        def convert_datetime(value):
            if value:
                return value.strftime("%Y-%m-%d %H:%M:%S")
            else:
                return ""

        d = {}
        for col in row.__table__.columns:
            if isinstance(col.type, TIMESTAMP):
                value = convert_datetime(getattr(row, col.name))
            else:
                value = getattr(row, col.name)
            d[col.name] = value
        return d


if __name__ == '__main__':
    print(Utils.now())
    pass
