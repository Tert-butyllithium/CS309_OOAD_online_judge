## 在config里面需要配置的东西：

![](api_1.png)

## 需要导入的包

import datetime

import flask

import hashlib

import logzero

import logging

import socket

import psutil

import pymysql

import queue

import threading

import time



## 接口

在使用接口之前，需要开进程运行 `\judger\service\app.py`

命令行传参，参数分别为端口，ip地址和是否开启debug model

![1570698189139](api_2.png)

默认参数为 5000, localhost, false

可以只传前两个或者前一个。



所有的request都用POST的形式，其他形式不被接受

所有的request都需要带上一个header, 格式如下

```json
{
	'Cs309-Token': sha256(token)
}
```



### start

request:  `/api/start/`

不需要带data



### new_task

request: `/api/judge/`

```
{
	'solution_id': 给个id， string or int 应该都可以
}
```

注意本接口调用之前必须先调用start