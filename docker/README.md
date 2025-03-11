部署步骤1~3：

1. 创建`docker-compose.yml`变量文件`.env`(首次部署需要创建，后续按需要更新对应的变量)
    - 参照`.env.example`配置创建`.env`作为`docker-compose.yml`中使用的变量
    - 创建`.env`
   ```shell
   vim .env
   ```

2. Nginx配置`/ExileTestPlatformServer/docker/volumes/nginx/exile_platform.conf`
    - 修改`server_name`为对应的ip或域名
    - 修改`listen`端口号(可选),同时需要修改`docker-compose.yml`中nginx的端口

3. 执行`docker-compose.yml`构建

    - `-p exile_test_platform`别名

   ```shell
   docker compose -p exile_test_platform up -d
   ```

其他：

- 执行`Dockerfile`构建(仅构建服务端)

  ```shell
  docker build -t 'exile_platform_server' .
  docker run -d -p 8000:8000 exile_platform_server
  ```

打包为`.tar`,上传到服务器(按需要执行)

- 打包

   ```shell
   docker save -o exile_platform_server.tar exile_test_platform-api:latest
   ```

- 导入

   ```shell
   docker load -i exile_platform_server.tar
   ```