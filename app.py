import hashlib
import base64
import aiohttp
from sanic import Sanic
from sanic.response import json as sanic_json

from config import Config
from core.model import SQLiteModel
from core.schema import init_sqlite

app = Sanic(__name__)
SQLITE_MODEL = SQLiteModel()

init_sqlite()  # 初始化


async def send_requstes(method="GET", **kwargs):
    async with aiohttp.request(method, **kwargs) as response:
        # content_type=None 是因为aiohttp默认会校验 response headers 里的content-type: text会直接报错，
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
        return msg(msg='上传记录存在！', url=format_pic_url(file_name))

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

    # 添加记录
    SQLITE_MODEL.add_one_record(name=file_name)

    if '已存在' in str(result):
        return msg(msg='文件已经存在！', url=format_pic_url(file_name))
    else:
        return msg(msg='上传成功！', url=format_pic_url(file_name))


#     {
#     "hello":{
#         "content":{
#             "name":"dc1a4b3c1d0da45574bb558bddc6c5eb.jpg",
#             "path":"store/dc1a4b3c1d0da45574bb558bddc6c5eb.jpg",
#             "size":1150,
#             "sha":"def96c4ab0971338aba7f8da8a5c8d0bfa25d3f3",
#             "type":"file",
#             "url":"https://gitee.com/api/v5/repos/EngiGu/imagestore/contents/store/dc1a4b3c1d0da45574bb558bddc6c5eb.jpg",
#             "html_url":"https://gitee.com/EngiGu/imagestore/blob/back/store/dc1a4b3c1d0da45574bb558bddc6c5eb.jpg",
#             "download_url":"https://gitee.com/EngiGu/imagestore/raw/back/store/dc1a4b3c1d0da45574bb558bddc6c5eb.jpg",
#             "_links":{
#                 "self":"https://gitee.com/api/v5/repos/EngiGu/imagestore/contents/store/dc1a4b3c1d0da45574bb558bddc6c5eb.jpg",
#                 "html":"https://gitee.com/EngiGu/imagestore/blob/back/store/dc1a4b3c1d0da45574bb558bddc6c5eb.jpg"
#             }
#         },
#         "commit":{
#             "sha":"9c0bd21854302edca2dc924daa1bd6b3132e866b",
#             "author":{
#                 "name":"EngiGu",
#                 "date":"2020-02-07T17:15:26+08:00",
#                 "email":"451292130@qq.com"
#             },
#             "committer":{
#                 "name":"Gitee",
#                 "date":"2020-02-07T17:15:26+08:00",
#                 "email":"noreply@gitee.com"
#             },
#             "message":"upload AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAQAABILAAASCwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABaAAAAHy8pACIcHAspUTs+Nm1QbTp0VXw0a01oKEo3NiISFgciICAAAAAAAAAAAAAAAAAAAAAAAEANGwBNAAQBMD85IyxEOmQ/fGGxZ6ai8XSjyP90ndH/c6TE/mKjme07d1yUKC4qFStAOAAAAAAAAAAAADMyNAA4ICsKKV9JbyB+WNs3hGP9d6bK/2Jp8f9NT/j/SUvz/05Q9f9ocvT/cqq9/jt4XJIfAAAFMy0vADUqLgBGACYDKVQ7fh2HUvgfiVb/aqmq/19l/f9DRu//Rknz/0VJ7v9FSe//Q0b1/2hy+f9jpJvtKU06OzBVRQAsT0EALkg+OR6LXOoYk1P/NIVa/3mY4P9HRur/R0n3/0VH6P9HSfn/RUfo/0ZI8/9KSun/dqDO/zp1WIJB86oAFbRzACdkS30Zpm3/F6tu/zCLZf9KeZv/NFyg/zVbnv81XZ//NV6h/zVcnv81XqD/Nlee/lhtmNdAaVZv////AAD/oQAmXz+WGZVX/xmTU/8aiEn/GZFT/xmRUf8ahkX/GpBQ/xmXV/8aiEj/GZJR/x2CS/wtPDCKMyovIjIrLgAZllkAKFtCehuOU/8Ym1v/F6dp/xiWV/8Yl1j/F6do/xiYWP8Zk1P/GKJj/xiWVf8efErwL0A3RzQtMQszMzMALUxAAC9FPDMfjF/lF6xt/xieX/8Xp2j/F6hp/xifYP8XrG3/GKVm/xenaP8Ypmr/JHRStjgdKg0yNTUAAAAAADUnLQBVAAACKVdBcR96R/UZkVH/GY5N/xmNTP8ZkFD/GY1M/xmPTv8aiUv/Im1C3C5ANDspVToAOBonAAAAAAAAAAAANSYqADsOHQYrTTtgIX9Y0ByUYPkZn2X/Gads/xqZYf8dj17yJWxLtC86LzgA/00APBkuAAAAAAAAAAAAAAAAAAAAAABHBBEAcgAAADQxMRosU0NTKGRMfSdoTYkpYEpzLko/QTgiKwwoQjoAZAAYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//8AAP//AAD8BwAA4AMAAMABAACAAQAAgAEAAIABAACAAQAAgAEAAIADAACABwAAwA8AAOAfAAD//wAA//8AAA== by api",
#             "tree":{
#                 "sha":"a80cbd9068cc93db10325cc2ba1abd0ddda637ca",
#                 "url":"https://gitee.com/api/v5/repos/EngiGu/imagestore/git/trees/a80cbd9068cc93db10325cc2ba1abd0ddda637ca"
#             },
#             "parents":[
#                 {
#                     "sha":"6bf173e9edde1f32176f99a0065740b55f63a0da",
#                     "url":"https://gitee.com/api/v5/repos/EngiGu/imagestore/commits/6bf173e9edde1f32176f99a0065740b55f63a0da"
#                 }
#             ]
#         }
#     }
# }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, workers=Config.API_SERVER_WORKERS)
