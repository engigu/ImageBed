class Config:

    ############## GITEE配置 ##############
    # GITEE 用户授权码, 获取请打开 https://gitee.com/api/v5/swagger 授权复制出现的access_token
    ACCESS_TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxx'
    # OWNER 仓库所属空间地址(企业、组织或个人的用户名)
    OWNER = 'jake'
    # repo 仓库名字
    REPO = 'repo_name'
    # BRANCH 仓库分支(如果不存在的分支，需要提前建好)
    BRANCH = 'banch_name'
    # PATH 分支里的路径(如果要放在一个不存在的路径，最好也提前建好, 如果是根目录写/)
    STROE_PATH = 'your/images/path'
    ############## GITEE配置 ##############

    ############## API_SERVER配置 ##############
    # 是否只能上传图片文件(启用后端api的格式校验)
    ONLY_UPLOAD_IMG_FILES = True
    # API server worker数
    API_SERVER_WORKERS = 4
    # API server port （
    # 项目里有两个端口，如果你想整个web+api一起跑， 不要改这个端口（改动需要改动对应的nginx配置、dockerfile);
    # 如果只跑后端api，根据需要改端口
    # ）
    API_SERVER_PORT = 8000
    # sqlite 数据库路径
    SQLITE_URI = 'sqlite:///sqlite_db/sqlite.db'
    ############## API_SERVER配置 ##############
