Python SDK及客户端
==================

|readthedocs|

我们提供了方便调用MOS API的Python SDK以及基于该SDK实现的客户端。

安装
----

使用pip安装
~~~~~~~~~~~
在命令行下可以直接使用pip进行安装::

    sudo pip install mosclient

从源码安装
~~~~~~~~~~
从 `github下载最新版 <https://github.com/meituan/mcsapi_python/archive/master.zip>`_ 代码并解压，或者执行如下命令获取源码::

    git clone https://github.com/meituan/mcsapi_python.git

进入mcsapi_python目录执行下述命令安装客户端可执行文件climos以及相应的python SDK::

    python setup.py install

访问MOS控制台的 `API页面 <https://mos.meituan.com/console/#api>`_ 获得API入口URL、ACCESS Key和Secret。

使用Python SDK
--------------

通过mosclient.client.Client生成客户端实例，API接口说明实现参见 `SDK API文档 <http://mcsapi-python.readthedocs.org/zh_CN/latest/client.html>`_ 。

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

安装客户端软件后，执行以下步骤开始使用MOS API Python客户端。

设置环境变量
~~~~~~~~~~~~

在MOS控制台 `API页面 <https://mos.meituan.com/console/#api>`_ 获取个人的MOS ACCESS Key和Secret，以及API入口URL。设置如下环境变量

::

   export MOS_ACCESS=4ba303cc17454cc7904e044db2a3c912
   export MOS_SECRET=2952f821201341a38978ac4a4a292ce8
   export MOS_URL=https://mosapi.meituan.com/mcs/v1

执行climos客户端
~~~~~~~~~~~~~~~~

climos是命令行的客户端工具，用户可以在终端运行，下面的示例是如何使用命令行创建一台机器：

::

    # 输出climos命令行工具帮助信息
    > climos help

    # 获取当前余额
    > climos GetBalance

    # 列出所有可用的虚拟机镜像模板，选择一个模板，并记下模板ID，如8e76df8f-3476-4eed-8469-ed22daa1334c (templateID)
    > climos DescribeTemplates

    # 列出所有可用的虚拟机类型，选择一个类型，并记下类型ID，如C1_M1 (instanceTypeID)
    > climos DescribeInstanceTypes

    # 创建虚拟机，注意需要帐户中有足够余额
    > climos CreateInstance 8e76df8f-3476-4eed-8469-ed22daa1334c C1_M1


.. |readthedocs| image:: https://readthedocs.org/projects/mcsapi-python/badge/?version=latest
   :target: http://mcsapi-python.readthedocs.org/zh_CN/latest/
   :alt: Documentation Status
