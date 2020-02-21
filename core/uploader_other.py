#
# 主要放一些免费的不用在意质量的api
#

import base64
import re
from aiohttp import FormData

from core.uploader_base import BaseUploder
from core.utils import Utils
from config import Config


class G360Uploader(BaseUploder):
    name = '360'

    def __init__(self, ):
        super().__init__()

    async def format_pic_url(self, filename):
        return 'https://ps.ssl.qhmsg.com/{filename}'.format(filename=filename)

    async def upload(self, file, filename, raw_filename):
        # file 二进制文件
        file_content = base64.b64encode(file).decode()
        data = FormData()
        data.add_field('upload', '')
        data.add_field('imgurl', '')
        data.add_field('base64image', 'data:image/png;base64,%s' % file_content)
        data.add_field('submittype', 'screenshot')
        data.add_field('src', 'st')
        kwargs = {
            'url': 'https://st.so.com/stu',
            'data': data,
            'headers': {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36",
            },
        }
        res_page = await self.send_requstes('POST', return_json=False, **kwargs)
        image_name = re.findall(r'id="initParam" type="text/data" data-query="" data-total="0" data-imgkey="(.*?)" data-tags', res_page, re.S)
        return image_name

    async def deal_upload_result(self, result, filename):
        # 处理上传结果
        if not result:
            # 正则匹配为空list
            raise NameError('360没有返回图片名！')
        url = await self.format_pic_url(result[0])
        # 结果正常
        need_add_record = False
        return 0, '上传成功！', url, need_add_record

    async def init_server(self, sqlite_model):
        # 初始化
        print('2. starting pull blob images...')
        print('all done.')
