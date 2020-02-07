import asyncio
from app import send_requstes
from core.schema import init_sqlite
from core.model import SQLiteModel
from config import Config


async def get_all_blob_tree():
    # 主要是获取所有的blob目录
    kwargs = {
        'url': 'https://gitee.com/api/v5/repos/{owner}/{repo}/contents/{path}?access_token={access_token}&ref={branch}'.format(
            owner=Config.OWNER, repo=Config.REPO, branch=Config.BRANCH, access_token=Config.ACCESS_TOKEN, path=Config.STROE_PATH
        ),
    }
    return await send_requstes('GET', **kwargs)


async def main_steps():
    # 1. 删除db，重新实例化db
    init_sqlite()
    print('1. has inited sqlite.db')

    # 2. 拉取出仓库目录下已经存在的文件, 将记录插入sqlite
    print('2. starting pull blob images...')
    SQL_MODEL = SQLiteModel()
    result = await get_all_blob_tree()
    # print(result)
    i = 0
    for r in result:
        SQL_MODEL.add_one_record(name=r['name'])
        i += 1
    print('2. complete all recrod to sqlite [%s/%s]' % (i, i))
    print('all done.')

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_steps())
