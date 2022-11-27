# Nginx安装

## 安装虚拟机

1. 下载centos 7的安装镜像，使用Windows的Hyper-v虚拟机功能，安装虚拟机。
2. 为虚拟机设置静态IP
   - 由于默认虚拟交换机每次开机会随机重置IP，因此新建虚拟交换机；![图 1](.assets_IMG/Nginx%E5%AE%89%E8%A3%85/IMG_20221123-160006146.png)  
   - 在网络适配器中设置IP范围![图 2](.assets_IMG/Nginx%E5%AE%89%E8%A3%85/IMG_20221123-160326239.png)  
   - 在虚拟机设置选择新建的交换机![图 3](.assets_IMG/Nginx%E5%AE%89%E8%A3%85/IMG_20221123-160500343.png)  
   - 在虚拟机设置静态IP，编辑 `/etc/sysconfig/network-scripts/ifcfg-eth0`

      ```ini
      TYPE=Ethernet
      PROXY_METHOD=none
      BROWSER_ONLY=no
      BOOTPROTO=static # 静态
      DEFROUTE=yes
      IPV4_FAILURE_FATAL=no
      IPV6INIT=yes
      IPV6_AUTOCONF=yes
      IPV6_DEFROUTE=yes
      IPV6_FAILURE_FATAL=no
      IPV6_ADDR_GEN_MODE=stable-privacy
      NAME=eth0
      UUID=99ca693a-e9e8-4a1c-b3f2-dfec0572a917
      DEVICE=eth0
      ONBOOT=yes
      IPADDR=192.168.148.2 # 地址
      PREFIX=24 # 掩码长度
      GATEWAY=192.168.148.1 # 网关
      DNS1=114.114.114.114 # DNS
      DNS2=223.5.5.5
      ```

   - 重启网络服务 `systemctl restart network`

## Nginx版本

- 开源版本 nginx.org 功能较少，基本就是反向代理服务器
- 商用版本nginx plus www.nginx.com
- Openresty
- Tengine 淘宝

## Nginx开源版安装

1. 下载 `wget  http://nginx.org/download/nginx-1.23.2.tar.gz`
2. 解压 `tar zxvf nginx-1.23.2.tar.gz`
3. 进入解压目录`cd nginx-1.23.2`，查看编译条件`./configure`，提示`error: C compiler cc is not found`
4. 安装gcc
5. 使用 `./configure --prefix=/usr/local/nginx`将nginx安装到指定目录
6. `error: the HTTP rewrite module requires the PCRE library.
You can either disable the module by using --without-http_rewrite_module
option, or install the PCRE library into the system, or build the PCRE library
statically from the source with nginx by using --with-pcre=<path> option.` 安装pcre库 `yum install -y pcre pcre-devel`
7. `yum install -y zlib zlib-devel`
8. `make`
9. `make install`

## Nginx启动

1. 进入目录`cd /usr/local/nginx/sbin`
2. 运行 `./nginx`

### 防火墙

- 查看防火墙状态
`firewall-cmd --state`
- 停止firewall
`systemctl stop firewalld.service`
- 禁止firewall开机启动
`systemctl disable firewalld.service`
- 放行端口
`firewall-cmd --zone=public --add-port=80/tcp --permanent`
- 查看已放行端口
`firewall-cmd --list-port`
- 重启防火墙
`firewall-cmd --reload`

### 启动

```ini
./nginx   # 启动
./nginx -s stop  # 快速停止
./nginx -s quit  # 优雅关闭，在退出前完成已经接受的连接请求
./nginx -s reload   # 重新加载配置
```

## 将Nginx安装成系统服务

1. 创建服务脚本nginx.service `vi /usr/lib/systemd/system/nginx.service`
2. 内容如下(注意路径要对应，这里的安装路径是/usr/local/nginx/sbin)：

    ```ini
    [Unit]
    Description=nginx - web server
    After=network.target remote-fs.target nss-lookup.target

    [Service]
    Type=forking
    PIDFile=/usr/local/nginx/logs/nginx.pid
    ExecStartPre=/usr/local/nginx/sbin/nginx -t -c /usr/local/nginx/conf/nginx.conf
    ExecStart=/usr/local/nginx/sbin/nginx -c /usr/local/nginx/conf/nginx.conf
    ExecReload=/usr/local/nginx/sbin/nginx -s reload
    ExecStop=/usr/local/nginx/sbin/nginx -s stop
    ExecQuit=/usr/local/nginx/sbin/nginx -s quit
    PrivateTmp=true

    [Install]
    WantedBy=multi-user.target
    ```

3. 重新加载系统服务 `systemctl daemon-reload` 然后将上面运行的nginx关闭
4. 启动服务 `systemctl start nginx.service`
5. 开机启动 `systemctl enable nginx.service`