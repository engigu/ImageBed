#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : github.py.py
# @Author: guq  
# @Date  : 2022/4/19
# @Desc  :


import base64
import hashlib
from core.uploader_base import BaseUploader, init_server_decor


class GithubUploader(BaseUploader):
    name = 'github'
    is_repo = True

    def __init__(self, access_token, owner, repo, branch, store_path, user_cdn='jsdelivr'):
        self.access_token = access_token
        self.owner = owner.lower()
        self.repo = repo
        self.branch = branch
        self.store_path = store_path
        self.user_cdn = user_cdn  # jsdelivr CDN加速
        self.headers = {
            "Authorization": "token %s" % access_token,
            "Accept": "application/vnd.github.v3+json"
        }
        super().__init__()

    async def format_pic_url(self, filename):
        fullname = filename
        # fullname = SQLiteModel.get_fullname_by_name(filename, upload_way=self.name)
        if not self.user_cdn:
            self.user_cdn = 'jsdelivr'
        cdn = self.user_cdn

        if cdn == 'jsdelivr':
            # https://cdn.jsdelivr.net/gh/engigu/ReadLogs/static/logviewer.gif
            path = 'https://cdn.jsdelivr.net/gh/{owner}/{repo}@{branch}/{path}/{fullname}'.format(
                owner=self.owner,
                repo=self.repo,
                path=self.store_path,
                fullname=fullname,
                branch=self.branch
            )
        elif cdn == 'staticaly':
            # https://cdn.staticaly.com/gh/engigu/resources/images/2022/05/28/f2a10f482d97c53142301438debe0119.png
            path = 'https://cdn.staticaly.com/gh/{owner}/{repo}/{branch}/{path}/{fullname}'.format(
                owner=self.owner,
                repo=self.repo,
                path=self.store_path,
                fullname=fullname,
                branch=self.branch
            )
        else:
            # 默认的github
            # https://raw.githubusercontent.com/EngiGu/resources/images/2.txt
            path = 'https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}/{fullname}'.format(
                owner=self.owner,
                repo=self.repo,
                path=self.store_path,
                fullname=fullname,
                branch=self.branch
            )
        return path.replace('///', '/')

    def git_blob_hash(self, data):
        if isinstance(data, str):
            data = data.encode()
        data = b'blob ' + str(len(data)).encode() + b'\0' + data
        h = hashlib.sha1()
        h.update(data)
        return h.hexdigest()

    async def upload(self, file, filename, raw_filename):
        # file 二进制文件
        file_content = base64.b64encode(file).decode()
        sha = self.git_blob_hash(file)
        url = 'https://api.github.com/repos/{owner}/{repo}/contents/{path}/{fullname}'.format(
            owner=self.owner, repo=self.repo, path=self.store_path, fullname=filename
        ).replace('///', '/')
        kwargs = {
            'url': url,
            'json': {
                "message": self.format_upload_info(filename),
                "committer": {
                    "name": "image bot",
                    "email": "image_bot@sooko.club"
                },
                "content": file_content,
                "branch": self.branch,
                'sha': sha
            },
            'headers': self.headers
        }
        return await self.send_requstes('PUT', **kwargs)

    async def deal_upload_result(self, result, filename):
        # 处理上传结果
        url = await self.format_pic_url(filename)
        need_add_record = False
        if 'committer' not in str(result):
            # 上传出现异常
            return -1, str(result), str(result), need_add_record
        else:
            # 结果正常
            need_add_record = True
            return 0, '上传成功！', url, need_add_record

    async def get_all_blob_tree(self):
        # 主要是获取所有的blob目录
        kwargs = {
            'url': 'https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1'.format(
                owner=self.owner, repo=self.repo, branch=self.branch, access_token=self.access_token,
                path=self.store_path
            ),
        }
        return await self.send_requstes('GET', **kwargs)

    async def processing_tree_data(self, tree):
        result = []
        for blob in tree:
            path = blob.get('path', '')
            filename = path.split("/")[-1]
            if len(filename.split('.')[0]) == 32:
                result.append({'name': filename, 'fullname': path})
        return result

    async def do_data(self):
        result = await self.get_all_blob_tree()
        result = await self.processing_tree_data(result.get('tree', []))
        return result

    @init_server_decor
    async def init_server(self, sqlite_model):
        # 初始化
        print('2. starting pull blob images...')
        result = await self.do_data()
        i = 0
        for file in result:
            sqlite_model.add_one_record(name=file['name'], upload_way=self.name, fullname=file['fullname'])
            i += 1
            print('3.. complete all recrod to sqlite [%s/%s]' % (i, i), end='\r')
        print('\nall done.', )
