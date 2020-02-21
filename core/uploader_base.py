import hashlib
import aiohttp


class BaseUploder:
    name = 'base_uploader'

    async def send_requstes(self, method="GET", return_json=True, **kwargs):
        async with aiohttp.request(method, **kwargs) as response:
            # content_type=None 是因为aiohttp默认会校验 response headers 里的content-type: text会直接报错，
            # 直接关闭校验
            if return_json:
                return await response.json(content_type=None)
            return await response.text()

    async def generate_file_hash(self, file):
        return hashlib.md5(file).hexdigest()

    async def format_pic_url(self, filename):
        pass

    async def upload(self, file, filename):
        pass

    async def deal_upload_result(self, result):
        # 处理上传结果
        pass
