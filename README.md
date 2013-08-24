# MCS API Python Binding #

我们提供了方便调用MCS API的Python Library以及基于该Libary实现的客户端。

## 安装 ##

从本站下载mcsapi_python代码，解压，进入目录执行下述命令安装。将安装客户端可执行文件climos以及相应的python library。

    python setup.py install

## Python Library ##

通过mosclient.client.Client生成客户端实例，API接口实现参见mosclient/v1/client.py。

示例代码如下：

```python
    import mosclient
    
    version = '1'
    key = 'MOS_ACCESS_KEY'
    secret = 'MOS_ACCESS_SECRET'
    url = 'https://mcsapi.meituan.com:8333/'
    
    cli = mosclient.client.Client(version, key, secret, url)

    types = cli.GetBalance()
    print types
```

## Python客户端 ##

安装客户端软件后，执行以下步骤开始使用MCS API Python客户端。

1\. 在MOS帐户页面获取个人的MOS ACCESS Key和Secret，以及API入口URL，设置如下环境变量：

    export MOS_ACCESS=4ba303cc17454cc7904e044db2a3c912
    export MOS_SECRET=2952f821201341a38978ac4a4a292ce8
    export MOS_URL=https://10.168.44.160:8883

2\. 执行climos客户端

    climos help
    climos DescribeTemplates
