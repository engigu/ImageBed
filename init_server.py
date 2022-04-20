import asyncio
from core.schema import init_sqlite
from core.model import SQLiteModel
from core.loader import __UPLODER_MAPS__


async def main_steps():
    # 1. 删除db，重新实例化db
    init_sqlite()
    print('1. has inited sqlite.db')

    # 2. 拉取出仓库目录下已经存在的文件, 将记录插入sqlite
    SQL_MODEL = SQLiteModel()
    for uploader in __UPLODER_MAPS__.values():
        await uploader.init_server(sqlite_model=SQL_MODEL)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_steps())
