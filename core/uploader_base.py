import hashlib
import aiohttp

from core.utils import Utils


def init_server_decor(func):
    def wrapper(self, *args, **kwargs):
        self.log_info('*' * 30)
        self.log_info('1. start init files data to db...')
        result = func(self, *args, **kwargs)
        return result

    return wrapper


class BaseUploader:
    name = 'base_uploader'
    is_repo = False

    async def send_requstes(self, method="GET", return_json=True, **kwargs):
        async with aiohttp.request(method, **kwargs) as response:
            # content_type=None 是因为aiohttp默认会校验 response headers 里的content-type: text会直接报错，
            # 直接关闭校验
            if return_json:
                return await response.json(content_type=None)
            return await response.text()

    def log_info(self, info, end=''):
        if end:
            print(f'[{self.name}] {info}', end=end)
        else:
            print(f'[{self.name}] {info}')

    def format_upload_info(self, filename):
        now = Utils.now(return_datetime=False)
        return f"upload at {now}"

    async def generate_fullname(self, filename):
        if self.is_repo:
            return '{day}/{filename}'.format(
                filename=filename, day=Utils.now(return_datetime=True).strftime('%Y/%m/%d')
            )
        return filename

    async def generate_file_hash(self, file):
        return hashlib.md5(file).hexdigest()

    async def format_pic_url(self, filename):
        raise NotImplementedError

    async def upload(self, file, filename, raw_filename):
        raise NotImplementedError

    async def deal_upload_result(self, result, filename):
        # 处理上传结果
        raise NotImplementedError

    async def do_data(self):
        return []

    @init_server_decor
    async def init_server(self, sqlite_model):
        # 初始化
        self.log_info('2. starting pull blob images...')
        result = await self.do_data()
        i = 0
        for file in result:
            sqlite_model.add_one_record(name=file['name'], upload_way=self.name, fullname=file['fullname'])
            i += 1
            self.log_info('3. complete all recrod to sqlite [%s/%s]' % (i, i), end='\r')
        self.log_info('', end='\n')
        self.log_info('4. done')
        print()
