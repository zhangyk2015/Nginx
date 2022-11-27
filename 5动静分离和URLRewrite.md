# 动静分离和URLRewrite

## 动静分离

为了提高网站的响应速度，减轻程序服务器（Tomcat，Jboss等）的负载，对于静态资源，如图片、js、css等文件，可以在反向代理服务器中进行缓存，这样浏览器在请求一个静态资源时，代理服务器就可以直接处理，而不用将请求转发给后端服务器。对于用户请求的动态文件，如servlet、jsp，则转发给Tomcat，Jboss服务器处理，这就是动静分离。即动态文件与静态文件的分离。

### 动静分离原理

动静分离可通过location对请求url进行匹配，将网站静态资源（HTML，JavaScript，CSS，img等文件）与后台应用分开部署，提高用户访问静态代码的速度，降低对后台应用访问。通常将静态资源放到nginx中，动态资源转发到tomcat服务器中。

### 用法

在server 配置中新增location，将静态资源代理至自身服务器。

- 正则

  ```ini
    ^ ：匹配输入字符串的起始位置
    $ ：匹配输入字符串的结束位置
    * ：匹配前面的字符零次或多次。如“ol*”能匹配“o”及“ol”、“oll”
    + ：匹配前面的字符一次或多次。如“ol+”能匹配“ol”及“oll”、“olll”，但不能匹配“o”
    ? ：匹配前面的字符零次或一次，例如“do(es)?”能匹配“do”或者“does”，”?”等效于”{0,1}”
    . ：匹配除“\n”之外的任何单个字符，若要匹配包括“\n”在内的任意字符，请使用诸如“[.\n]”之类的模式
    \ ：将后面接着的字符标记为一个特殊字符或一个原义字符或一个向后引用。如“\n”匹配一个换行符，而“\$”则匹配“$”
    \d ：匹配纯数字
    {n} ：重复 n 次
    {n,} ：重复 n 次或更多次
    {n,m} ：重复 n 到 m 次
    [] ：定义匹配的字符范围
    [c] ：匹配单个字符 c
    [a-z] ：匹配 a-z 小写字母的任意一个
    [a-zA-Z0-9] ：匹配所有大小写字母或数字
    () ：表达式的开始和结束位置
    | ：或运算符  //例(js|img|css)
  ```

- location正则
  
  ```ini
    //location大致可以分为三类
    精准匹配：location = /{}
    一般匹配：location /{}
    正则匹配：location ~/{}
    //location常用的匹配规则：
    = ：进行普通字符精确匹配，也就是完全匹配。
    ^~ ：表示前缀字符串匹配（不是正则匹配，需要使用字符串），如果匹配成功，则不再匹配其它 location。
    ~ ：区分大小写的匹配（需要使用正则表达式）。
    ~* ：不区分大小写的匹配（需要使用正则表达式）。
    !~ ：区分大小写的匹配取非（需要使用正则表达式）。
    !~* ：不区分大小写的匹配取非（需要使用正则表达式）。
    //优先级
    首先精确匹配 =
    其次前缀匹配 ^~
    其次是按文件中顺序的正则匹配 ~或~*
    然后匹配不带任何修饰的前缀匹配
    最后是交给 / 通用匹配
  ```

- 说明

  ```ini
    （1）location = / {}
    =为精确匹配 / ，主机名后面不能带任何字符串，比如访问 / 和 /data，则 / 匹配，/data 不匹配
    再比如 location = /abc，则只匹配/abc ，/abc/或 /abcd不匹配。若 location  /abc，则即匹配/abc 、/abcd/ 同时也匹配 /abc/。

    （2）location / {}
    因为所有的地址都以 / 开头，所以这条规则将匹配到所有请求 比如访问 / 和 /data, 则 / 匹配， /data 也匹配，
    但若后面是正则表达式会和最长字符串优先匹配（最长匹配）

    （3）location /documents/ {}
    匹配任何以 /documents/ 开头的地址，匹配符合以后，还要继续往下搜索其它 location
    只有其它 location后面的正则表达式没有匹配到时，才会采用这一条

    （4）location /documents/abc {}
    匹配任何以 /documents/abc 开头的地址，匹配符合以后，还要继续往下搜索其它 location
    只有其它 location后面的正则表达式没有匹配到时，才会采用这一条

    （5）location ^~ /images/ {}
    匹配任何以 /images/ 开头的地址，匹配符合以后，停止往下搜索正则，采用这一条

    （6）location ~* \.(gif|jpg|jpeg)$ {}
    匹配所有以 gif、jpg或jpeg 结尾的请求
    然而，所有请求 /images/ 下的图片会被 location ^~ /images/ 处理，因为 ^~ 的优先级更高，所以到达不了这一条正则

    （7）location /images/abc {}
    最长字符匹配到 /images/abc，优先级最低，继续往下搜索其它 location，会发现 ^~ 和 ~ 存在

    （8）location ~ /images/abc {}
    匹配以/images/abc 开头的，优先级次之，只有去掉 location ^~ /images/ 才会采用这一条

    （9）location /images/abc/1.html {}
    匹配/images/abc/1.html 文件，如果和正则 ~ /images/abc/1.html 相比，正则优先级更高

    优先级总结：
    (location =) > (location 完整路径) > (location ^~ 路径) > (location ~,~* 正则顺序) > (location 部分起始路径) > (location /)
  ```

## URLRewrite

rewrite是实现URL重写的关键指令，根据regex(正则表达式)部分内容，重定向到repacement，结尾是flag标记。

在location中新增rewrite

```conf
rewrite ^/test.html$ /index.html?testParam=3 break;

//也可以用正则表达式的形式：
rewrite ^/[0-9]+.html$ /index.html?testParam=$1 break; //$1表示第一个匹配的字符串 
```

![图 2](.assets_IMG/%E5%8A%A8%E9%9D%99%E5%88%86%E7%A6%BB%E5%92%8CURLRewrite/IMG_20221125-221308710.png)  

## 负载均衡+URLRewrite

让内网服务器只能通过Nginx代理服务器访问
添加防火墙
`firewall-cmd --permanent --add-rich-rule="rule family="ipv4" source address="192.168.8.102" port protocol="tcp" port="8080" accept"`
移除防火墙
`firewall-cmd --permanent --remove-rich-rule="rule family="ipv4" source address="192.168.8.102" port protocol="tcp" port="8080" accept"`

