# -*- coding: utf-8 -*-

import re

from mosclient.common import utils
from mosclient.common.client import BaseClient


def match_duration(string):
    if re.match(r'^\d+[HhMm]$', string):
        return True
    return False


class Client(BaseClient):
    """
    MCS API client (v1)

    :param access: 指定MOS API access key
    :type access: string
    :param secret: 指定MOS API secret
    :type secret: string
    :param url: MOS API访问URL
    :type url: string
    :param format: 指定返回数据格式xml或者json，缺省为xml
    :type format: string
    :param timeout: 超时秒数，缺省为300秒
    :type timeout: int
    :param debug: 是否输出debug信息，缺省为False
    :type debug: bool
    """

    def DescribeInstanceTypes(self, limit=0, offset=0, filters=None):
        """ 获取所有虚拟机类型

        :param limit: 最大返回数量，用于分页控制
        :type limit: int
        :param offset: 返回偏移量，用于分页控制
        :type offset: int
        :param filters: 过滤条件，key/value分别指定过滤字段名称和值，支持的字段名称为：name, status
        :type filters: dict
        :returns: InstanceTypeSet，包含系统支持的虚拟机类型列表
        """
        kwargs = {}
        self.parse_list_params(limit, offset, filters, kwargs)
        val = self.request(**kwargs)
        return val['InstanceTypeSet']

    def DescribeTemplates(self):
        """ 获得所有虚拟机模板

        :returns: 模板列表
        """
        val = self.request()
        return val['TemplateSet']

    def GetBalance(self):
        """ 获取帐户余额

        :returns: 帐户余额和最近更新时间
        """
        val = self.request()
        return val

    def DescribeInstances(self, ids=None, names=None, limit=0, offset=0,
                                filters=None):
        """ 获得所有虚拟机

        :param ids: 期望获取的虚拟机ID列表
        :type ids: list
        :param names: 期望获取信息的虚拟机名称列表
        :type names: list
        :param limit: 最多返回数量
        :type limit: int
        :param offset: 返回虚拟机的偏移量，用于分页显示
        :type offset: int
        :param filters: 过滤器，一个dict，包含过滤字段名和值，可能过滤字段为：name, status
        :type filters: dict

        :returns: InstanceSet，包含虚拟机列表
        """
        kwargs = {}
        if isinstance(ids, list) and len(ids) > 0:
            kwargs['InstanceId'] = ids
        if isinstance(names, list) and len(names) > 0:
            kwargs['InstanceName'] = names
        self.parse_list_params(limit, offset, filters, kwargs)
        val = self.request(**kwargs)
        return val['InstanceSet']

    def DescribeInstanceVolumes(self, iid, limit=0, offset=0, filters=None):
        """ 获取指定虚拟机的虚拟磁盘信息

        :param iid: 虚拟机ID
        :type iid: string
        :param limit: 最大返回数量，用于分页控制
        :type limit: int
        :param offset: 返回的偏移量，用于分页控制
        :type offset: int
        :param filters: 返回结果过滤条件，由dict的key/value指定过滤字段名和值

        :returns: InstanceVolumeSet，包含虚拟机磁盘列表
        """
        kwargs = {}
        kwargs['InstanceId'] = iid
        self.parse_list_params(limit, offset, filters, kwargs)
        val = self.request(**kwargs)
        return val['InstanceVolumeSet']

    def DescribeInstanceNetworkInterfaces(self, iid, limit=0, offset=0,
                                                filters=None):
        """ 获取指定虚拟机的网络接口（虚拟网卡）信息

        :param iid: 虚拟机ID
        :type iid: string
        :param limit: 最大返回数量，用于分页控制
        :type limit: int
        :param offset: 返回的偏移量，用于分页控制
        :type offset: int
        :param filters: 返回结果过滤条件，由dict的key/value指定过滤字段名和值

        :returns: InstanceNetworkInterfaceSet，包含虚拟机网络接口列表
        """
        kwargs = {}
        kwargs['InstanceId'] = iid
        self.parse_list_params(limit, offset, filters, kwargs)
        val = self.request(**kwargs)
        return val['InstanceNetworkInterfaceSet']

    def RenewInstance(self, iid, duration=None):
        """ 虚拟机租期续费

        :param iid: 虚拟机ID
        :type iid: string
        :param duration: 续费租期，缺省为'1M'，即一个月
        :type duration: string
        """
        kwargs = {}
        kwargs['InstanceId'] = iid
        if duration is not None:
            if match_duration(duration):
                kwargs['Duration'] = duration
            else:
                raise Exception('Illegal duration %s' % duration)
        self.request(**kwargs)

    def GetInstanceContractInfo(self, iid):
        """ 获取虚拟机的租期信息

        :param iid: 虚拟机ID
        :type iid: string

        :returns: 虚拟机租期信息，包含过期时间、自动删除时间
        """
        kwargs = {}
        kwargs['InstanceId'] = iid
        return self.request(**kwargs)

    def CreateInstance(self, imageid, itype, duration=None, name=None,
            keypair=None, datadisk=None, bandwidth=None):
        """ 创建虚拟机

        :param imageid: 系统模板ID
        :type imageid: string
        :param itype: 虚拟机类型ID
        :type itype: string
        :param duration: 虚拟机租期, 缺省为'1M'，即一个月
        :type duration: string
        :param name: 虚拟机名称(可选)
        :type name: string
        :param keypair: 虚拟机使用的SSH密钥ID
        :type keypair: string
        :param datadisk: 指定创建虚拟机使用的额外数据盘，单位为GB
        :type datadisk: int
        :param bandwidth: 指定创建虚拟机使用的额外带宽，单位为Mbps
        :type bandwidth: int

        :returns: 创建成功的虚拟机信息
        """
        kwargs = {}
        kwargs['ImageId'] = imageid
        kwargs['InstanceType'] = itype
        if duration is not None:
            if match_duration(duration):
                kwargs['Duration'] = duration
            else:
                raise Exception('Illegal duration format')
        if name is not None:
            kwargs['InstanceName'] = name
        if keypair is not None:
            kwargs['KeyName'] = keypair
        if datadisk is not None:
            kwargs['ExtraExtDisksize'] = int(datadisk)
        if bandwidth is not None:
            kwargs['ExtraExtBandwidth'] = int(bandwidth)
        val = self.request(**kwargs)
        return val['Instance']

    def DescribeInstanceStatus(self, iid):
        """ 获取虚拟机的状态

        :param iid: 虚拟机ID
        :type iid: string

        :returns: 虚拟机状态字符串
        """
        kwargs = {}
        kwargs['InstanceId'] = iid
        val = self.request(**kwargs)
        return val['InstanceStatus']

    def GetPasswordData(self, iid, key_file=None):
        """ 获取虚拟机的Login帐户信息

        :param iid: 虚拟机ID
        :type iid: string
        :param key_file: 私钥文件路径，路过虚拟机使用了SSH密钥，需要指定私钥解密password
        :type key_file: string

        :returns: 虚拟机Login信息，包含帐户名称、密码，如果使用SSH密钥，则还包含密钥ID和名称
        """
        kwargs = {}
        kwargs['InstanceId'] = iid
        val = self.request(**kwargs)
        if 'passwordData' in val and 'keypairName' in val:
            if key_file is None:
                raise Exception('Password is encrypted, please speecify '
                        'private key of keypair %s' % val['keypairName'])
            else:
                with open(key_file) as f:
                    key = f.read()
                    val['passwordData'] = utils.decrypt_base64(key,
                                                    val['passwordData'])
        return val

    def StartInstance(self, iid):
        """ 启动虚拟机

        :param iid: 虚拟机ID
        :type iid: string
        """
        kwargs = {}
        kwargs['InstanceId'] = iid
        self.request(**kwargs)

    def StopInstance(self, iid, force=False):
        """ 停止虚拟机

        :param iid: 虚拟机ID
        :type iid: string
        :param force: 是否强制停止虚拟机
        :type param: bool
        """
        kwargs = {}
        kwargs['InstanceId'] = iid
        if force:
            kwargs['Force'] = force
        self.request(**kwargs)

    def RebootInstance(self, iid):
        """ 重启虚拟机

        :param iid: 虚拟机ID
        :type iid: string
        """
        kwargs = {}
        kwargs['InstanceId'] = iid
        self.request(**kwargs)

    def TerminateInstance(self, iid):
        """ 删除虚拟机

        :param iid: 虚拟机ID
        :type iid: string
        """
        kwargs = {}
        kwargs['InstanceId'] = iid
        self.request(**kwargs)

    def RebuildInstanceRootImage(self, iid, image_id=None):
        """ 重置虚拟机系统磁盘

        :param iid: 虚拟机ID
        :type iid: string
        :param image_id: 将虚拟机系统磁盘用指定镜像模板重置，如果无该参数，则使用原镜像模板重置
        :type image_id: string
        """
        kwargs = {}
        kwargs['InstanceId'] = iid
        if image_id is not None and len(image_id) > 0:
            kwargs['ImageId'] = image_id
        self.request(**kwargs)

    def ChangeInstanceType(self, iid, itype, duration=None,
                            datadisk=None, bandwidth=None):
        """ 更改虚拟机类型

        :param iid: 虚拟机ID
        :type iid: string
        :param itype: 指定更改的虚拟机类型
        :type itype: string
        :param duration: 指定更改后的初始租期，缺省为'1M'，即一个月
        :type duration: string
        :param datadisk: 指定创建虚拟机使用的额外数据盘，单位为GB
        :type datadisk: int
        :param bandwidth: 指定创建虚拟机使用的额外带宽，单位为Mbps
        :type bandwidth: int

        """
        kwargs = {}
        kwargs['InstanceId'] = iid
        kwargs['InstanceType'] = itype
        if duration is not None:
            if match_duration(duration):
                kwargs['Duration'] = duration
            else:
                raise Exception('IIlegal duration format')
        if datadisk is not None:
            kwargs['ExtraExtDisksize'] = int(datadisk)
        if bandwidth is not None:
            kwargs['ExtraExtBandwidth'] = int(bandwidth)

        self.request(**kwargs)

    def GetInstanceMetadata(self, iid):
        """ 获取虚拟机的metadata

        :param iid: 虚拟机ID
        :type iid: string

        :returns: 一个dict包含虚拟机所有metadata的key/value
        """
        kwargs = {}
        kwargs['InstanceId'] = iid
        val = self.request(**kwargs)
        return val['InstanceMetadata']

    def PutInstanceMetadata(self, iid, data):
        """ 修改虚拟机的metadata

        :param iid: 虚拟机ID
        :type iid: string
        :param data: 需要增加或修改的metadata信息
        :type data: dict
        """
        kwargs = {}
        kwargs['InstanceId'] = iid
        names = []
        values = []
        for k, v in data.iteritems():
            names.append(k)
            values.append(v)
        kwargs['Name'] = names
        kwargs['Value'] = values
        self.request(**kwargs)

    def DescribeKeyPairs(self, limit=0, offset=0, filters=None):
        """ 获取用户的SSH密钥对

        :param limit: 最大返回数量，用于分页控制
        :type limit: int
        :param offset: 返回偏移量，用于分页控制
        :type offset: int
        :param filters: 过滤条件，key/value分别指定过滤字段名称和值，支持的字段名称为：name
        :type filters: dict

        :returns: KeyPairSet, 包含SSH密钥对列表
        """
        kwargs = {}
        self.parse_list_params(limit, offset, filters, kwargs)
        val = self.request(**kwargs)
        return val['KeyPairSet']

    def ImportKeyPair(self, name, pubkey):
        """ 导入一个用户的SSH公钥，并创建一个SSH密钥对

        :param name: 密钥对名称
        :type name: string
        :param pubkey: SSH公钥信息
        :type pubkey: string

        :returns: 创建的SSH密钥对信息
        """
        kwargs = {}
        kwargs['KeyName'] = name
        kwargs['PublicKeyMaterial'] = pubkey
        val = self.request(**kwargs)
        return val['KeyPair']

    def DeleteKeyPair(self, kid):
        """ 删除一个SSH密钥对

        :param kid: 密钥对ID
        :type kid: string
        """
        kwargs = {}
        kwargs['KeyName'] = kid
        self.request(**kwargs)

    def CreateTemplate(self, iid, name, notes=None):
        """ 保存虚拟机的模板

        :param iid: 虚拟机ID
        :type iid: string
        :param name: 模板名称
        :type name: string
        :param notes: 保存模板的说明
        :type notes: string

        :returns:  请求是否成功
        """
        kwargs = {}
        kwargs['InstanceId'] = iid
        kwargs['Name'] = name
        if notes is not None:
            kwargs['Notes'] = notes
        val = self.request(**kwargs)
        return val

    def DeleteTemplate(self, tid):
        """ 删除一个模板

        :param tid: 模板ID
        :param tid: string
        """

        kwargs = {}
        kwargs['TemplateId'] = tid
        self.request(**kwargs)
