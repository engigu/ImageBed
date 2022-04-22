#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : github.py.py
# @Author: guq  
# @Date  : 2022/4/19
# @Desc  :


from aiohttp import FormData

from core.uploader_base import BaseUploader, init_server_decor


class CodingUploader(BaseUploader):
    name = 'coding'
    is_repo = True

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
        # filename  -> fullname
        pices = filename.split('/')
        filename = pices[-1]
        pre_path = '/'.join(pices[:-1])
        lastCommitSha = await self.get_last_commit_sha()
        data = FormData()
        data.add_field('file', file, filename=filename)
        data.add_field('message', self.format_upload_info(filename))
        data.add_field('lastCommitSha', lastCommitSha)
        data.add_field('newRef', '')

        kwargs = {
            'url': 'https://{owner}.coding.net/api/user/{owner}/project/{repo}/depot/{repo}/git/upload/{branch}/{path}/{pre_path}'.format(
                owner=self.owner, repo=self.repo, path=self.store_path, branch=self.branch, pre_path=pre_path
            ).replace('///', '/'),
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

    async def do_data(self):
        result = await self.get_coding_tree_blob_file()
        return [
            {'name': file['name'], 'fullname': file['path']}
            for file in result['data']['files']
        ]
