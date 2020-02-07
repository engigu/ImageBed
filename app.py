import hashlib
import aiohttp
from sanic import Sanic
from sanic.response import json as sanic_json

from config import Config

app = Sanic(__name__)


async def send_requstes(method="GET", **kwargs):
    async with aiohttp.request(method, **kwargs) as response:
        # content_type=None 是因为aio默认会校验 response headers 里的content-type: text会直接报错，
        # 直接关闭校验
        return await response.json(content_type=None)


# async def init_server():
#     # 主要是获取所有的图片
#     kwargs = {
#         'url': 'https://gitee.com/api/v5/repos/{owner}/{repo}/git/trees/{branch}?access_token={access_token}&recursive={recursive}'.format(
#             owner=Config.OWNER, repo=Config.REPO, branch=Config.BRANCH, access_token=Config.ACCESS_TOKEN, recursive=Config.RECURSIVE
#         ),
#     }
#     res = await send_requstes('GET', **kwargs)
#     print(res)

def msg(code=0, msg='ok!'):
    return sanic_json({'code':code, 'msg': msg})



@app.route("/api/upload", methods=['POST'])
async def upload(request):
    # 文件上传
    # https://gitee.com/api/v5/swagger#/postV5ReposOwnerRepoContentsPath
    pic_file = request.files.get('file')  # type body name
    print(pic_file.name, pic_file.type)
    # 文件类型校验
    if Config.ONLY_UPLOAD_IMG_FILES and 'image' not in pic_file.type:
            return msg(code=-1, msg='请务必只上传图片文件！')   

    file_name = '1.txt'
    file_content = 'JXU4RkQ5JXU5MUNDJXU2NjJGJXU4OTgxJXU1MkEwJXU1QkM2JXU3Njg0JXU1MTg1JXU1QkI5JXVGRjAx'
    kwargs = {
        'url': 'https://gitee.com/api/v5/repos/{owner}/{repo}/contents/{path}/{file_name}'.format(
            owner=Config.OWNER, repo=Config.REPO, path=Config.STROE_PATH, file_name=file_name
        ),
        'data': {
            "access_token": Config.ACCESS_TOKEN, "content": file_content,
            "message": "upload %s by api" % file_content, "branch": Config.BRANCH
        }
    }
    result = await send_requstes('POST', **kwargs)

    if '已存在' in str(result):
        return sanic_json({'code': 0, 'msg': '文件已经存在！'})

    return sanic_json({"hello": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, workers=4)
