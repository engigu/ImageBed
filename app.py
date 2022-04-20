from sanic import Sanic
from sanic import response

from config import Config
from core.model import SQLiteModel
from core.utils import Utils
from core.loader import __UPLODER_MAPS__, SUPPORT_UPLOAD_WAYS

app = Sanic(__name__)
SQLITE_MODEL = SQLiteModel()


def msg(code=0, msg='ok!', url=''):
    return response.json(
        {'code': code, 'msg': msg, 'url': url},
        headers={
            'X-Served-By': 'sanic',
        },
        status=200
    )


app.static('/', './web/index.html')
app.static('/js', './web/js')
app.static('/css', './web/css')
app.static('/images', './web/images')
app.static('/favicon.ico', './web/favicon.ico')


@app.route("/api/upload", methods=['POST'])
async def upload(request):
    try:
        # 文件上传
        pic_file = request.files.get('file')  # type body name
        # 文件类型校验
        if Config.ONLY_UPLOAD_IMG_FILES and 'image' not in pic_file.type:
            return msg(code=-1, msg='请务必只上传图片文件！')

        upload_way = request.form.get('uploadWay') or ''
        upload_way = upload_way.lower()

        # upload_way 校验
        if upload_way not in SUPPORT_UPLOAD_WAYS or not upload_way:
            return msg(code=-1, msg='uploadWay错误！', url='uploadWay错误！')

        # uploader 获取
        uploader = __UPLODER_MAPS__.get(upload_way, None)
        if not uploader:
            return msg(code=-1, msg='找不到对用的uploder！', url='找不到对用的uploder！')

        file_hash = await uploader.generate_file_hash(pic_file.body)
        raw_suffix = pic_file.name.split('.')[-1]
        file_name = '%s.%s' % (file_hash, raw_suffix)

        record = SQLITE_MODEL.get_one_record(
            name=file_name, upload_way=upload_way)
        if record:
            # 之前有记录
            return msg(msg='之前上传过哟～', url=await uploader.format_pic_url(file_name))

        # 上传
        result = await uploader.upload(file=pic_file.body, filename=file_name, raw_filename=pic_file.name)
        code, show_msg, url, need_add_record = await uploader.deal_upload_result(result, filename=file_name)
        if need_add_record:
            # 添加记录
            SQLITE_MODEL.add_one_record(name=file_name, upload_way=upload_way)

        return msg(code=code, msg=show_msg, url=url)
    except Exception as e:
        show_msg = '内部错误！error：%s' % str(e)
        return msg(code=-1, msg=show_msg, url=show_msg)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=Config.API_SERVER_PORT,
        workers=Config.API_SERVER_WORKERS
    )
