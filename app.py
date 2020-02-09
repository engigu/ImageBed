import hashlib
import base64
import aiohttp
from sanic import Sanic
from sanic.response import json as sanic_json

from config import Config
from core.model import SQLiteModel

app = Sanic(__name__)
SQLITE_MODEL = SQLiteModel()


async def send_requstes(method="GET", **kwargs):
    async with aiohttp.request(method, **kwargs) as response:
        # content_type=None 是因为aiohttp默认会校验 response headers 里的content-type: text会直接报错，
        # 直接关闭校验
        return await response.json(content_type=None)


def msg(code=0, msg='ok!', url=''):
    return sanic_json({'code': code, 'msg': msg, 'url': url})


def generate_file_hash(file):
    return hashlib.md5(file).hexdigest()


def format_pic_url(file_name):
    return 'https://gitee.com/{owner}/{repo}/raw/{branch}/{path}/{file_name}'.format(
        owner=Config.OWNER, repo=Config.REPO, path=Config.STROE_PATH, file_name=file_name, branch=Config.BRANCH
    )


@app.route("/api/upload", methods=['POST'])
async def upload(request):
    # 文件上传
    # https://gitee.com/api/v5/swagger#/postV5ReposOwnerRepoContentsPath
    pic_file = request.files.get('file')  # type body name
    # 文件类型校验
    if Config.ONLY_UPLOAD_IMG_FILES and 'image' not in pic_file.type:
        return msg(code=-1, msg='请务必只上传图片文件！')

    file_hash = generate_file_hash(pic_file.body)
    file_name = '%s.%s' % (file_hash, pic_file.name.split('.')[-1])
    file_content = base64.b64encode(pic_file.body).decode()

    record = SQLITE_MODEL.get_one_record(name=file_name)
    if record:
        # 之前有记录
        return msg(msg='之前上传过哟～', url=format_pic_url(file_name))

    kwargs = {
        'url': 'https://gitee.com/api/v5/repos/{owner}/{repo}/contents/{path}/{file_name}'.format(
            owner=Config.OWNER, repo=Config.REPO, path=Config.STROE_PATH, file_name=file_name
        ),
        'data': {
            "access_token": Config.ACCESS_TOKEN, "content": file_content,
            "message": "upload %s by api" % pic_file.name, "branch": Config.BRANCH
        }
    }
    result = await send_requstes('POST', **kwargs)

    if '已存在' in str(result):
        # 添加记录
        SQLITE_MODEL.add_one_record(name=file_name)
        return msg(msg='文件已经存在！', url=format_pic_url(file_name))
    elif 'html_url' not in str(result):
        # 出现异常了
        return msg(code=-1, msg=str(result), url=str(result))
    else:
        # 添加记录
        SQLITE_MODEL.add_one_record(name=file_name)
        return msg(msg='上传成功！', url=format_pic_url(file_name))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.API_SERVER_PORT,
            workers=Config.API_SERVER_WORKERS)
