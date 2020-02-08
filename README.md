# ImageBed

![输入图片说明](https://images.gitee.com/uploads/images/2020/0208/092300_da8cfc9a_1346635.png "屏幕截图.png")
![输入图片说明](https://images.gitee.com/uploads/images/2020/0208/094443_a0d34bdb_1346635.png "屏幕截图.png")
写`Markdown`的时候总是要做图片的引用，使用`github`速度又不是很友好，看到国内代码托管平台`gitee`， 有`openapi`([`gitee`.`swagger`](https://gitee.com/api/v5/swagger))可以调用，于是写了这个基于`仓库`的图床，主要放一些自己文字里的图片。

页面很low，可以只跑api, 后端框架使用`sanic`，自己也是第一次使用这个异步框架

# 环境
  - python3.7.2
  - sanic
  - 更多详见`requirements.txt`


# 说明
1. 整个项目一起运行

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
    docker run -d -p 8000:8000 --name imagebed imagebed-server
    ```
    如果要把`sqlite`保存在外部，需要挂载`-v {yourpath}:/app/sqlite_db`

    b. 请求参数
    ```curl
    curl -X POST 'http:/ip:8000/api/upload' -d '{file: (binary)}'
    ```

# TODO
  - 页面优化
  - 支持剪贴板上传
  
