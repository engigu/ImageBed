class Config:
    ############## GITHUB配置 ##############
    # Github 用户授权码, access_token获取参见github个人设置
    GITHUB_ACCESS_TOKEN = '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'
    # OWNER 仓库所属空间地址(企业、组织或个人的用户名)
    GITHUB_OWNER = 'engigu'
    # repo 仓库名字
    GITHUB_REPO = 'resources'
    # BRANCH 仓库分支(如果不存在的分支，需要提前建好)
    GITHUB_BRANCH = 'images'
    # PATH 分支里的路径(如果要放在一个不存在的路径，最好也提前建好, 如果是根目录写/)
    GITHUB_STORE_PATH = '/'
    CDN_USE = 'staticaly'
    # staticaly jsdelivr github
    ############## Coding配置 ##############

    ############## GITEE配置 ##############
    # GITEE 用户授权码, 获取请打开 https://gitee.com/api/v5/swagger 授权复制出现的access_token
    GITEE_ACCESS_TOKEN = '10593078507388a667a0a5ba80e48540'
    # OWNER 仓库所属空间地址(企业、组织或个人的用户名)
    GITEE_OWNER = 'EngiGu'
    # repo 仓库名字
    GITEE_REPO = 'imagestore'
    # BRANCH 仓库分支(如果不存在的分支，需要提前建好)
    GITEE_BRANCH = 'back'
    # PATH 分支里的路径(如果要放在一个不存在的路径，最好也提前建好, 如果是根目录写/)
    GITEE_STORE_PATH = 'store'
    ############## GITEE配置 ##############

    ############## Coding配置 ##############
    # Coding 用户授权码
    CODING_ACCESS_TOKEN = '50e7534296748606f6715c9346a3d756cf7648ce'
    # OWNER 仓库所属空间地址(企业、组织或个人的用户名)
    CODING_OWNER = 'EngiGu'
    # repo 仓库名字
    CODING_REPO = 'imagestore'
    # BRANCH 仓库分支(如果不存在的分支，需要提前建好)
    CODING_BRANCH = 'back'
    # PATH 分支里的路径(如果要放在一个不存在的路径，最好也提前建好, 如果是根目录写/)
    CODING_STORE_PATH = 'store'
    ############## Coding配置 ##############

    ############## Minio配置 ##############
    # MINIO token
    MINIO_ACCESS_TOKEN = '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'
    # MINIO secret
    MINIO_SECRET = 'engigu'
    # bucket
    MINIO_BUCKET = 'resources'
    # server地址
    MINIO_SERVER = 'images'
    ############## Coding配置 ##############


    ############## API_SERVER配置 ##############
    # 是否只能上传图片文件(启用后端api的格式校验)
    ONLY_UPLOAD_IMG_FILES = True
    # API server worker数
    API_SERVER_WORKERS = 4
    # API server port （
    # 项目里有两个端口，如果你想整个web+api一起跑， 不要改这个端口（改动需要改动对应的nginx配置、dockerfile);
    # 如果只跑后端api，根据需要改端口
    # ）
    API_SERVER_PORT = 9999
    # sqlite 数据库路径
    SQLITE_URI = 'sqlite:///sqlite_db/sqlite.db'
    ############## API_SERVER配置 ##############


