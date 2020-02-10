from aiohttp import FormData
# import requests
import asyncio, aiohttp

async def send_requstes( method="GET", **kwargs):
    async with aiohttp.request(method, **kwargs) as response:
        # content_type=None 是因为aiohttp默认会校验 response headers 里的content-type: text会直接报错，
        # 直接关闭校验
        return await response.json(content_type=None)

headers = {
    # "Accept-Encoding": "gzip, deflate, br",
    # "Accept-Language": "zh-CN,zh;q=0.9,it;q=0.8",
    # "Connection": "keep-alive",
    "Cookie": "_ga=GA1.2.418561365.1576566628; code=Conan%3Dtrue%2Cartifacts-overview%3Dtrue%2Cartifacts-properties%3Dtrue%2Cartifacts-strategy%3Dtrue%2Casync-blocked%3Dtrue%2Cci-micro-frontend%3Dtrue%2Ccoding-flow%3Dfalse%2Ccomposer-proxy%3Dtrue%2Cgit-micro-fe%3Dfalse%2Cjenkins-ci%3Dfalse%2Cmicro%3Dfalse%2Cmobile-layout-test%3Dfalse%2Cnew-git%3Dfalse%2Cstatic-website%3Dtrue%2Csvn-depot%3Dfalse%2Ctencent-cloud-object-storage%3Dtrue%2C095d5700; exp=89cd78c2; c=Conan%3Dtrue%2Cartifacts-overview%3Dtrue%2Cartifacts-properties%3Dtrue%2Cartifacts-strategy%3Dtrue%2Cci-micro-frontend%3Dtrue%2Ccomposer-proxy%3Dtrue%2Cstatic-website%3Dtrue%2C08005302; _gid=GA1.2.1094328747.1581226364; eid=f3bfd7d0-ecbe-430f-b5c8-2736e75bebcd; coding_demo_visited=1; __xr_token=XRT-b3e17b3d-d48e-4e77-b884-48078f43c030; C_CLIENT_ID=817f85e9-9b3b-43d8-aa96-1e6e0665a94a; sid=fa75211e-a8eb-474f-9ea8-0c489090930d; XSRF-TOKEN=072d415c988e90ff39850631c35576f0074dba82:1581302664880",
    # "Host": "engigu.coding.net",
    # "Origin": "https://engigu.coding.net",
    # "Referer": "https://engigu.coding.net/p/imagestore/d/imagestore/git/upload/master/",
    # "Sec-Fetch-Dest": "empty",
    # "Sec-Fetch-Mode": "cors",
    # "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36",
    # "X-XSRF-TOKEN": "072d415c988e90ff39850631c35576f0074dba82:1581302664880",
}

url = 'https://engigu.coding.net/api/user/EngiGu/project/imagestore/depot/imagestore/git/upload/master/'
file = '/home/sayheya/Pictures/2020-01-29 16-50-03 的屏幕截图.png'


# files = {
#     'filexx': ('cc.png', open(file, 'rb')),
#     'msg': ('message', '上传文件'),
#     'last': ('lastCommitSha', 'c77032da09f68b05a202b3223392346b75a7446a'),
#     'new': ('newRef', '')
# }
# r = requests.post(url, headers=headers, files=files)
# print(r.content.decode())


async def main_steps():
    data = FormData()
    data.add_field('file', open(file, 'rb'), filename='pp.png')
    data.add_field('message', '上传文件')
    data.add_field('lastCommitSha', 'c084054f981e63e8b5547f5e1c6715b5452a1637')
    data.add_field('newRef', '')
    kwargs = {
        'data': data,
        'headers': headers,
        'url': url
    }
    res = await send_requstes('POST', **kwargs)
    print('res', res)
    pass

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_steps())
