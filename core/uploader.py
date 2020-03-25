import base64
from aiohttp import FormData

from core.uploader_base import BaseUploder, init_server_decor
from core.utils import Utils
from config import Config


class GiteeUploader(BaseUploder):
    name = 'gitee'

    def __init__(self, access_token, owner, repo, branch, store_path):
        self.access_token = access_token
        self.owner = owner.lower()
        self.repo = repo
        self.branch = branch
        self.store_path = store_path
        super().__init__()

    async def format_pic_url(self, filename):
        return 'https://gitee.com/{owner}/{repo}/raw/{branch}/{path}/{filename}'.format(
            owner=self.owner,
            repo=self.repo,
            path=self.store_path,
            filename=filename,
            branch=self.branch
        )

    async def upload(self, file, filename, raw_filename):
        # file 二进制文件
        # https://gitee.com/api/v5/swagger#/postV5ReposOwnerRepoContentsPath
        file_content = base64.b64encode(file).decode()
        kwargs = {
            'url': 'https://gitee.com/api/v5/repos/{owner}/{repo}/contents/{path}/{filename}'.format(
                owner=self.owner, repo=self.repo, path=self.store_path, filename=filename
            ),
            'data': {
                "access_token": self.access_token,
                "content": file_content,
                "message": "upload %s at %s" % (raw_filename, Utils.now(return_datetime=False)),
                "branch": self.branch
            }
        }
        return await self.send_requstes('POST', **kwargs)

    async def deal_upload_result(self, result, filename):
        # 处理上传结果
        url = await self.format_pic_url(filename)
        need_add_record = False
        if '已存在' in str(result):
            need_add_record = True
            return 0, '文件已经存在！', url, need_add_record
        elif 'html_url' not in str(result):
            # 上传出现异常
            return -1, str(result), str(result), need_add_record
        else:
            # 结果正常
            need_add_record = True
            return 0, '上传成功！', url, need_add_record

    async def get_gitee_all_blob_tree(self):
        # 主要是获取所有的blob目录
        kwargs = {
            'url': 'https://gitee.com/api/v5/repos/{owner}/{repo}/contents/{path}?access_token={access_token}&ref={branch}'.format(
                owner=self.owner, repo=self.repo, branch=self.branch, access_token=self.access_token, path=self.store_path
            ),
        }
        return await self.send_requstes('GET', **kwargs)

    @init_server_decor
    async def init_server(self, sqlite_model):
        # 初始化
        print('2. starting pull blob images...')
        result = await self.get_gitee_all_blob_tree()
        i = 0
        for r in result:
            sqlite_model.add_one_record(name=r['name'], upload_way=self.name)
            i += 1
            print(
                '2. complete all recrod to sqlite [%s/%s]' % (i, i), end='\r')
        print('\nall done.',)


class CodingUploader(BaseUploder):
    name = 'coding'

    def __init__(self, token, owner, repo, branch, store_path):
        self.token = token
        self.owner = owner.lower()
        self.repo = repo
        self.branch = branch
        self.store_path = store_path
        self.headers = {
            "Authorization": "token %s" % token
        }
        super().__init__()

    async def format_pic_url(self, filename):
        return 'https://{owner}.coding.net/p/{repo}/d/{repo}/git/raw/{branch}/{path}/{filename}'.format(
            owner=self.owner,
            repo=self.repo,
            path=self.store_path,
            filename=filename,
            branch=self.branch
        )

    async def get_last_commit_sha(self):
        kwargs = {
            'url': 'https://{owner}.coding.net/api/user/{owner}/project/{repo}/depot/{repo}/git/upload/{branch}/{path}'.format(
                owner=self.owner, repo=self.repo, path=self.store_path, branch=self.branch
            ),
            'headers': self.headers
        }
        result = await self.send_requstes('GET', **kwargs)
        try:
            return result['data']['lastCommit']
        except Exception as e:
            print('get last commit error: %s, result: %s' %
                  (str(e), str(result)))

    async def upload(self, file, filename, raw_filename):
        # file 二进制文件
        lastCommitSha = await self.get_last_commit_sha()
        data = FormData()
        data.add_field('file', file, filename=filename)
        data.add_field('message', "upload %s at %s" %
                       (raw_filename, Utils.now(return_datetime=False)))
        data.add_field('lastCommitSha', lastCommitSha)
        data.add_field('newRef', '')
        kwargs = {
            'url': 'https://{owner}.coding.net/api/user/{owner}/project/{repo}/depot/{repo}/git/upload/{branch}/{path}'.format(
                owner=self.owner, repo=self.repo, path=self.store_path, branch=self.branch
            ),
            'data': data,
            'headers': self.headers,
        }
        return await self.send_requstes('POST', **kwargs)

    async def deal_upload_result(self, result, filename):
        # 处理上传结果
        url = await self.format_pic_url(filename)
        need_add_record = False
        print(result)
        if result['code'] == 0:
            # 结果正常
            need_add_record = True
            return 0, '上传成功！', url, need_add_record
        elif result['code'] == 1217:
            # 文件已存在
            need_add_record = True
            return 0, '文件已经存在！', url, need_add_record
        else:
            # 异常
            return -1, str(result['msg']), str(result['msg']), need_add_record

    async def get_coding_tree_blob_file(self):
        # 初始化
        kwargs = {
            'url': 'https://{owner}.coding.net/api/user/{owner}/project/{repo}/depot/{repo}/git/tree/{branch}/{path}'.format(
                owner=self.owner, repo=self.repo, path=self.store_path, branch=self.branch
            ),
            'headers': self.headers
        }
        result = await self.send_requstes('GET', **kwargs)
        return result

    @init_server_decor
    async def init_server(self, sqlite_model):
        # 初始化
        print('2. starting pull blob images...')
        result = await self.get_coding_tree_blob_file()
        i = 0
        for r in result['data']['files']:
            sqlite_model.add_one_record(name=r['name'], upload_way=self.name)
            i += 1
            print('2. complete all recrod to sqlite [%s/%s]' % (i, i), end='\r')
        print('\nall done.',)


# 其他接口
from core.uploader_other import (
    G360Uploader, SouGouUploader, BaiDuUploader,
    AliUploader
)


__UPLODER_MAPS__ = {
    GiteeUploader.name: GiteeUploader(
        access_token=Config.GITEE_ACCESS_TOKEN,
        owner=Config.GITEE_OWNER,
        repo=Config.GITEE_REPO,
        branch=Config.GITEE_BRANCH,
        store_path=Config.GITEE_STROE_PATH
    ),
    CodingUploader.name: CodingUploader(
        token=Config.CODING_ACCESS_TOKEN,
        owner=Config.CODING_OWNER,
        repo=Config.CODING_REPO,
        branch=Config.CODING_BRANCH,
        store_path=Config.CODING_STROE_PATH
    ),
    G360Uploader.name: G360Uploader(),
    SouGouUploader.name: SouGouUploader(),
    BaiDuUploader.name: BaiDuUploader(),
    AliUploader.name: AliUploader(),
}

SUPPORT_UPLOAD_WAYS = [name.lower() for name in __UPLODER_MAPS__.keys()]
