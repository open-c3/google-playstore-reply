# 用途说明

```
有的企业，在GooglePlay上有很多帐号和应用。这些帐号需要每天对用户在GooglePlay上的评论进行回复。
帐号多的情况下，需要登陆多个机器进行操作。

Open-C3提供了GooglePlay评论回复的管理功能。需要为每个帐号启动一个容器，评论的数据会同步到Open-C3。
在Open-C3上点击回复评论，请求会转发到对应的容器。

同时为了避免IP关联。部署本插件的机器是一个独立的机器，并且需要关闭外网功能，确保机器不能访问外部网络。
容器通过代理来对外访问google的接口。
```

# 使用说明

## 安装git命令
```
yum install -y git
```

## 下载代码
```
cd /data
git clone https://github.com/open-c3/google-playstore-reply.git
```

## 安装docker环境
```
yum install -y yum-utils device-mapper-persistent-data lvm2
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum -y install docker-ce docker-ce-cli containerd.io
sudo systemctl start docker
docker -v
```

## 准备容器
```
cd docker
echo http://10.10.10.10 > c3addr
./load.sh 
```
注: c3addr中记录着open-c3的地址，load.sh加载镜像的时候会从open-c3上下载镜像文件。

### 镜像生成
```
在Open-C3的机器上，在相同的目录下执行./build.sh 会生成镜像。
执行./save.sh会把镜像提供到http服务中给本项目的插件下载。
```

## 准备git容器
```
cd docker/git
cp ../c3addr .
echo 10.10.10.10:1080 > socks 
./load.sh
```
注: 因为本机没有公网环境无法上网。这里提供了一个容器用来更新代码。

其中socks文件就是容器使用的socks代理。

### 镜像生成
```
在Open-C3的机器上，在相同的目录下执行./build.sh 会生成镜像。
执行./save.sh会把镜像提供到http服务中给本项目的插件下载。
``

## 关闭公网网络
```
避免存在不使用代理的情况下访问google的接口，请通过设置安全组等方式，禁止本机访问公网。
``

## 配置config.yaml
```
把本机的ip配置到config.yaml, 本插件给Open-C3上报数据时，同时会上包本机的IP，Open-C3上回复评论时候会把请求转发到该IP。
```
## 在Open-C3中添加appkey
```
# cat /data/open-c3-data/to3part.yml 
googleplay: 401b30e3b8b5d629635a5c613cdb7919
```

注: 其中googleplay是appname，401b30e3b8b5d629635a5c613cdb7919是appkey。具体内容可以自己设置

在配置服务的时候需要appname和appkey才能正常上报给Open-C3

## 启动服务
```
准备conf/com.foo.myapp/config.yaml文件
./start com.foo.myapp
```

注： 其中com.foo.myapp为包名，根据具体情况而定。
