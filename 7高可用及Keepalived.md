# 高可用及Keepalived

Keepalived软件起初是专为LVS负载均衡软件设计的，用来管理并监控LVS集群系统中各个服务节点的状态，后来又加入了可以实现高可用的VRRP功能。因此，Keepalived除了能够管理LVS软件外，还可以作为其他服务（例如：Nginx、Haproxy、MySQL等）的高可用解决方案软件。VRRP出现的目的就是为了解决静态路由单点故障问题的，它能够保证当个别节点宕机时，整个网络可以不间断地运行。所以，Keepalived 一方面具有配置管理LVS的功能，同时还具有对LVS下面节点进行健康检查的功能，另一方面也可实现系统网络服务的高可用功能。

> keepalived官网 [http://www.keepalived.org](http://www.keepalived.org)

## keepalived服务的三个重要功能

- 管理LVS负载均衡软件
- 实现LVS集群节点的健康检查中
- 作为系统网络服务的高可用性（failover）

## 安装keepalived

`yum install -y keepalived`

## 用法

在该实战中，101为主nginx，102为备用机，首先需要修改101和102的keepalived.conf配置

101的`/etc/keepalived/keepalived.conf`配置

```conf
! Configuration File for keepalived

global_defs {
   router_id LB_102 # 标记
}

vrrp_instance VI_102 {
    state MASTER # 主节点
    interface ens33 # 网卡名 ip addr查看
    virtual_router_id 51
    priority 100 #优先级
    advert_int 1 #间隔检测的时间
    # 同一个环境中存在多个keepalived组时，keeplive分组认证
    authentication {
        auth_type PASS
        auth_pass 1111
    }
    virtual_ipaddress {
        192.168.8.200
    }
}
```

`systemctl start keepalived`启动keepalived,查看ip发现多了虚拟ip192.168.8.200

102的keepalived.conf配置

```conf
! Configuration File for keepalived

global_defs {
   router_id LB_101
}

vrrp_instance VI_102 {
    state BACKUP
    interface ens33
    virtual_router_id 51
    priority 50
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 1111
    }
    virtual_ipaddress {
        192.168.8.200
    }
}
```

原理是虚拟IP漂移