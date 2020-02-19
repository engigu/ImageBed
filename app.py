import hashlib
import base64
import aiohttp
from sanic import Sanic
from sanic.response import json as sanic_json

from config import Config
from core.model import SQLiteModel
from core.utils import Utils
from core.uploader import UPLODER

app = Sanic(__name__)
SQLITE_MODEL = SQLiteModel()


def msg(code=0, msg='ok!', url=''):
    return sanic_json({'code': code, 'msg': msg, 'url': url})


@app.route("/api/upload", methods=['POST'])
async def upload(request):
    try:
        # 文件上传
        pic_file = request.files.get('file')  # type body name
        # 文件类型校验
        if Config.ONLY_UPLOAD_IMG_FILES and 'image' not in pic_file.type:
            return msg(code=-1, msg='请务必只上传图片文件！')

        file_hash = await UPLODER.generate_file_hash(pic_file.body)
        file_name = '%s.%s' % (file_hash, pic_file.name.split('.')[-1])

        record = SQLITE_MODEL.get_one_record(name=file_name)
        if record:
            # 之前有记录
            return msg(msg='之前上传过哟～', url=await UPLODER.format_pic_url(file_name))

        # 上传
        result = await UPLODER.upload(file=pic_file.body, filename=file_name, raw_filename=pic_file.name)
        code, show_msg, url, need_add_record = await UPLODER.deal_upload_result(result, filename=file_name)
        if need_add_record:
            # 添加记录
            SQLITE_MODEL.add_one_record(name=file_name)

        return msg(code=code, msg=show_msg, url=url)
    except Exception as e:
        return msg(code=-1, msg='内部错误！error：%s' % str(e), url='')
        

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.API_SERVER_PORT, workers=Config.API_SERVER_WORKERS)
