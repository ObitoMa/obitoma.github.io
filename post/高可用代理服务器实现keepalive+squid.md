---
title: 高可用代理服务器实现keepalive+squid
tags: [linux, 代理, 部署, 高可用]
categories: [技术分享]
excerpt: 之前单机部署了squid代理服务器，现在实现一下高可用。
date: 2025-10-22 9:36:00
---
## 〇、前言

之前单机部署了squid代理服务器，现在实现一下高可用。

还有自定义squid的error页面

准备：两台centos7（1C2GB）

​			三个可用IP，一主一备一虚拟IP（VIP）

## 一、安装squid(两台)

```shell
yum install squid -y
# 具体配置略
```

## 二、安装keepalived（两台）

### 1.安装

```shell
yum install -y keepalived
yum install -y net-tools
```

### 2.配置

```shell
# 先清空原先配置
echo "" > /etc/keepalived/keepalived.conf

# 开始编辑
vim /etc/keepalived/keepalived.conf
# 这边注意网卡名称（interface ens160）和自身IP还有VIP
! Configuration File for keepalived
global_defs {
  router_id 本机IP
}
vrrp_script chk_squid {
  script "/etc/keepalived/check_port.sh 3128"
  interval 2
  weight -20
}
vrrp_instance VI_1 {
  state BACKUP
  interface ens160
  virtual_router_id 251
  mcast_src_ip 本机IP
  priority 90
  advert_int 1
  authentication {
    auth_type PASS
    auth_pass 11111111
  }
  track_script {
    chk_squid
  }
  virtual_ipaddress {
    虚拟IP
  }
}


```

### 3.编写端口检测脚本(两台)

```shell
vim /etc/keepalived/check_port.sh

#!/bin/bash
if [ $# -eq 1 ] && [[ $1 =~ ^[0-9]+ ]];then
    [ $(netstat -lntp|grep ":$1 " |wc -l) -eq 0 ] && echo "[ERROR] squid may be not running!" && exit 1 || exit 0
else
    echo "[ERROR] need one port!"
    exit 1
fi

# 赋予执行权限
chmod +x /etc/keepalived/check_port.sh
```

### 4.启动服务

```shell
systemctl enable keepalived && systemctl start keepalived
```

## 三、自定义squid的error页面

```shell
# 页面文件位置如下/usr/share/squid/errors/zh-cn+/ERR_ACCESS_DENIED

[root@squid-slave zh-cn]# cat  ERR_ACCESS_DENIED

<html><head>
<meta type="copyright" content="Copyright (C) 1996-2016 The Squid Software Foundation and contributors">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>错误: 不能获取请求的 URL</title>
<style type="text/css"><!--
 %l

body
:lang(fa) { direction: rtl; font-size: 100%; font-family: Tahoma, Roya, sans-serif; float: right; }
:lang(he) { direction: rtl; }
 --></style>
</head><body id="%c">
<div id="titles">
<h1>错误</h1>
<h2>您所请求的网址（URL）未授权</h2>
</div>
<hr>

<div id="content">
<p>当尝试请求返回 URL内容时遇到下面的错误：<a href="%U">%U</a></p>

<blockquote id="error">
<p><b>访问被拒绝。</b></p>
</blockquote>

<p>Access control configuration prevents your request from being allowed at this time. Please contact your service provider if you feel this is incorrect.</p>

<p>请联系马春旺。工号：***** 邮箱：****** </p>
<br>
</div>

<hr>
<div id="footer">
<p>Powered by 五星电器基础架构部</p>
<!-- %c -->
</div>
</body></html>

[root@squid-slave zh-cn]# systemctl restart squid
```

重启后即可看到如下：

![image-20210125134350921](https://gitee.com/ma_chun_wang/md_picture/raw/master/img/image-20210125134350921.png)