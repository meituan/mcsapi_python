MCS API Python SDK及客户端
==========================

我们提供了方便调用MCS API的Python SDK以及基于该SDK实现的客户端。

安装
----

从 `github下载mcsapi\_python <https://github.com/meituan/mcsapi_python/archive/master.zip>`_ 代码并解压，或者执行如下命令获取源码::

    git clone https://github.com/meituan/mcsapi_python

进入mcsapi_python目录执行下述命令安装客户端可执行文件climos以及相应的python SDK::

    python setup.py install

访问MOS管理界面的"`帐户-个人设置 <https://mos.meituan.com/dashboard/account#profile>`_"
页面获得API入口URL、ACCESS Key和Secret。

使用Python SDK
--------------

通过mosclient.client.Client生成客户端实例，API接口说明实现参见":doc:`mosclient/v1/client.py文档 <client>`"。

示例代码如下：

::

        import mosclient.client

        version = '1'
        key = 'MOS_ACCESS_KEY'
        secret = 'MOS_ACCESS_SECRET'
        url = 'https://mosapi.meituan.com/mcs/v1'

        cli = mosclient.client.Client(version, key, secret, url)

        balance = cli.GetBalance()
        print balance


使用Python客户端
----------------

安装客户端软件后，执行以下步骤开始使用MCS API Python客户端。

1. 在MOS帐户页面获取个人的MOS ACCESS
Key和Secret，以及API入口URL，设置如下环境变量：

::

    export MOS_ACCESS=4ba303cc17454cc7904e044db2a3c912
    export MOS_SECRET=2952f821201341a38978ac4a4a292ce8
    export MOS_URL=https://mosapi.meituan.com/mcs/v1

2. 执行climos客户端

::

    climos help
    climos DescribeTemplates

