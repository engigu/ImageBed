# ImageBed

![输入图片说明](https://images.gitee.com/uploads/images/2020/0208/092300_da8cfc9a_1346635.png "屏幕截图.png")
![输入图片说明](https://images.gitee.com/uploads/images/2020/0208/094443_a0d34bdb_1346635.png "屏幕截图.png")
写`Markdown`的时候总是要做图片的引用，使用`github`速度又不是很友好，看到国内代码托管平台`gitee`， 有`openapi`([`gitee`.`swagger`](https://gitee.com/api/v5/swagger))可以调用，于是写了这个基于`仓库`的图床，主要放一些自己文字里的图片。

页面很low，可以只跑api, 后端框架使用`sanic`，自己也是第一次使用这个异步框架。

图片文件名的生成使用文件的`md5值`，使用`sqlite.db`对上传记录进行持久化，并进行上传去重复判断。

欢迎大家提`issue`

##  Release

 - 2020.02.08 支持上传进度显示

## 环境
  - python3.7.2
  - sanic
  - 更多详见`requirements.txt`


## 说明
先拉取项目，更改`config.py`里的配置，修改参见下面的说明
```shell
git clone https://github.com/EngiGu/imagebed.git
```
1. 整个项目一起运行(**推荐**)

    a. 启动命令
    ```shell
    docker-compose up -d
    ```
    b. 如果是第一次运行，需要执行初始化(以后不用执行)
    ```shell
    docker-compose exec imagebed-server sh -c 'python init_server.py'
    ```
    c. 启动后访问`ip:9900`端口, 如果需要改动，修改`docker-compose.yml`里的端口

2. 只运行后端`api-server`
    
    a. 打包运行
     ```shell
    docker build -t imagebed-server .
    docker run -d -p 8000:8000 --name imagebed-server imagebed-server
    ```
    如果要把`sqlite`保存在外部，需要挂载`-v {yourpath}:/app/sqlite_db`
    
    b. 如果是第一次运行，需要执行初始化(以后不用执行)
    ```shell
    docker-compose exec imagebed-server sh -c 'python init_server.py'
    ```
    c. 请求参数
    ```curl
    curl -X POST 'http:/ip:8000/api/upload' -d '{file: (binary)}'
    ```

## 配置参数说明

```python
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
```



## TODO
  - 页面优化
  - 支持剪贴板上传
  - 防滥用
  
