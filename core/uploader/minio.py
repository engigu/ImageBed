#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : github.py.py
# @Author: guq  
# @Date  : 2022/4/19
# @Desc  :
import io

from minio import Minio

from core.uploader_base import BaseUploader, init_server_decor


class MinioUploader(BaseUploader):
    name = 'minio'
    is_repo = False

    def __init__(self, token, secret, bucket, server, alias_server):
        self.access_token = token
        self.secret = secret
        self.bucket = bucket
        self.server = server
        self.alias_server = alias_server
        self.minio = self.__init_server()
        super().__init__()

    def __init_server(self):
        return Minio(
            self.server,
            access_key=self.access_token,
            secret_key=self.secret,
            secure=False
        )

    async def format_pic_url(self, filename):
        return 'https://{server}/{bucket}/{filename}'.format(
            server=self.server if not self.alias_server else self.alias_server,
            bucket=self.bucket,
            filename=filename,
        )

    async def upload(self, file, filename, raw_filename):
        # file 二进制文件
        # filename  -> fullname
        return self.minio.put_object(self.bucket, filename, io.BytesIO(file), len(file))

    async def deal_upload_result(self, result, filename):
        # 处理上传结果
        url = await self.format_pic_url(filename)
        need_add_record = True
        # print(result)
        # if result['code'] == 0:
        #     # 结果正常
        #     need_add_record = True
        #     return 0, '上传成功！', url, need_add_record
        # elif result['code'] == 1217:
        #     # 文件已存在
        #     need_add_record = True
        #     return 0, '文件已经存在！', url, need_add_record
        # else:
        #     异常
        return 0, '上传成功！', url, need_add_record

    # async def get_coding_tree_blob_file(self):
    #     # 初始化
    #     kwargs = {
    #         'url': 'https://{owner}.coding.net/api/user/{owner}/project/{repo}/depot/{repo}/git/tree/{branch}/{path}'.format(
    #             owner=self.owner, repo=self.repo, path=self.store_path, branch=self.branch
    #         ),
    #         'headers': self.headers
    #     }
    #     result = await self.send_requstes('GET', **kwargs)
    #     return result

    async def do_data(self):
        return [
        ]
