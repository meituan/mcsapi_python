# -*- coding: utf-8 -*-

import json

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

    def DescribeInstances(self, ids=None, names=None, limit=0, offset=0, filters=None, group=None, zone=None):
        """ 获得所有虚拟机

        :param ids: 期望获取的虚拟机ID列表
        :type ids: list
        :param names: 期望获取信息的虚拟机名称列表
        :type names: list
        :param group: 分组名称 or ID
        :type group: string
        :param zone: 指定创建虚拟机所在的数据中心, 可通过DescribeAvailabilityZones接口获取
        :type zone: string
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
        if group:
            kwargs['Group'] = group
        if zone is not None:
            kwargs['AvailabilityZoneId'] = zone
        self.parse_list_params(limit, offset, filters, kwargs)
        val = self.request(**kwargs)
        return val['InstanceSet']


    def SearchAssociatedAddresses(self, ids=None, names=None):
        """ 获得所有虚拟机的浮动IP绑定情况

        :param ids: 期望获取的虚拟机ID列表
        :type ids: list
        :param names: 期望获取信息的虚拟机名称列表
        :type names: list
        :returns: InstanceEipInfoSet，包含虚拟机eip绑定数量列表
        """
        kwargs = {}
        if isinstance(ids, list) and len(ids) > 0:
            kwargs['InstanceId'] = ids
        if isinstance(names, list) and len(names) > 0:
            kwargs['InstanceName'] = names
        val = self.request(**kwargs)
        return val['InstanceEipInfoSet']

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
            keypair=None, secgroup=None, datadisk=None, bandwidth=None,
            zone=None, nets=None):
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
        :param secgroup: 安全组ID
        :type secgroup: string
        :param datadisk: 指定创建虚拟机使用的额外数据盘，单位为GB
        :type datadisk: int
        :param bandwidth: 指定创建虚拟机使用的额外带宽，单位为Mbps
        :type bandwidth: int
        :param zone: 指定创建虚拟机所在的数据中心, 可通过DescribeAvailabilityZones接口获取
        :type zone: string
        :param vpcsubnetid: 指定虚拟专有网络中的子网
        :type vpcsubnetid: string
        :param vpcsubnetip: 指定子网的情况下,可自定义IP(必须在子网IP范围内)
        :type vpcsubnetip: string
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
        if secgroup is not None:
            kwargs['GroupId'] = secgroup
        if datadisk is not None:
            kwargs['ExtraExtDisksize'] = int(datadisk)
        if bandwidth is not None:
            kwargs['ExtraExtBandwidth'] = int(bandwidth)
        if zone is not None:
            kwargs['AvailabilityZoneId'] = zone
        if isinstance(nets, list) and len(nets) > 0:
            kwargs['Nets'] = nets
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

    def DescribeInstanceMetrics(self, iid=None):
        """ 查看虚拟机监控项

        :param iid: 虚拟机ID
        :type iid: string

        :returns: MetricSet，包含监控项列表
        """
        kwargs = {}
        if iid:
            kwargs['InstanceId'] = iid
        val = self.request(**kwargs)
        return val['MetricSet']

    def DescribeAlarmHistory(self, limit=0, offset=0, filters=None):
        """ 查看监控告警历史

        :param limit: 最大返回数量，用于分页控制
        :type limit: int
        :param offset: 返回偏移量，用于分页控制
        :type offset: int

        :returns: AlarmHistorySet，监控告警历史列表
        """
        kwargs = {}
        self.parse_list_params(limit, offset, filters, kwargs)
        val = self.request(**kwargs)
        return val['AlarmHistorySet']

    def CreateMetricAlarm(self, iid, metric, operator, threshold, description=None):
        """ 创建指标监控

        :param iid: 虚拟机ID
        :type iid: string
        :param metric: 监控指标名称
        :type metric: string
        :param operator: 判断操作符
        :type operator: string
        :param threshold: 监控阈值
        :type threshold: string
        :param description: 描述
        :type description: string

        :returns: 请求是否成功
        """
        kwargs = {}
        kwargs['InstanceId'] = iid
        kwargs['Metric'] = metric
        kwargs['Operator'] = operator
        kwargs['Threshold'] = threshold
        if description:
            kwargs['Description'] = description
        val = self.request(**kwargs)
        return val['MetricAlarm']

    def DescribeMetricAlarms(self):
        """ 查看指标监控

        :returns: MetricAlarmSet，指标监控列表
        """
        val = self.request()
        return val['MetricAlarmSet']

    def DeleteMetricAlarm(self, mid):
        """ 删除一个指标监控项

        :param mid: 监控项ID
        :type mid: string

        :returns: 请求是否成功
        """
        kwargs = {}
        kwargs['MonitorId'] = mid
        val = self.request(**kwargs)
        return val

    def DisableMetricAlarm(self, mid):
        """ 禁用一个指标监控项

        :param mid: 监控项ID
        :type mid: string

        :returns: 请求是否成功
        """
        kwargs = {}
        kwargs['MonitorId'] = mid
        val = self.request(**kwargs)
        return val

    def EnableMetricAlarm(self, mid):
        """ 启用一个指标监控项

        :param mid: 监控项ID
        :type mid: string

        :returns: 请求是否成功
        """
        kwargs = {}
        kwargs['MonitorId'] = mid
        val = self.request(**kwargs)
        return val

    def CreateAliveAlarm(self, iid, description=None):
        """ 创建主机存活监控

        :param iid: 虚拟机ID
        :type iid: string
        :param description: 描述
        :type description: string

        :returns: 请求是否成功
        """
        kwargs = {}
        kwargs['InstanceId'] = iid
        if description:
            kwargs['Description'] = description
        val = self.request(**kwargs)
        return val['AliveAlarm']

    def DescribeAliveAlarms(self):
        """ 查看主机存活监控

        :returns: AliveAlarmSet，包含主机存货监控列表
        """
        val = self.request()
        return val['AliveAlarmSet']

    def DeleteAliveAlarm(self, mid):
        """ 删除主机存活监控

        :param mid: 监控项ID
        :type mid: string

        :returns: 请求是否成功
        """
        kwargs = {}
        kwargs['MonitorId'] = mid
        val = self.request(**kwargs)
        return val

    def DisableAliveAlarm(self, mid):
        """ 禁用一个主机存活监控项

        :param mid: 监控项ID
        :type mid: string

        :returns: 请求是否成功
        """
        kwargs = {}
        kwargs['MonitorId'] = mid
        val = self.request(**kwargs)
        return val

    def EnableAliveAlarm(self, mid):
        """ 启用一个主机存活监控项

        :param mid: 监控项ID
        :type mid: string

        :returns: 请求是否成功
        """
        kwargs = {}
        kwargs['MonitorId'] = mid
        val = self.request(**kwargs)
        return val

    def CreateTCPAlarm(self, iid, port, description=None):
        """ 创建TCP监控

        :param iid: 虚拟机ID
        :type iid: string
        :param port: tcp端口
        :type port: int
        :param description: 描述
        :type description: string

        :returns: 请求是否成功
        """
        kwargs = {}
        kwargs['InstanceId'] = iid
        kwargs['Port'] = port
        if description:
            kwargs['Description'] = description
        val = self.request(**kwargs)
        return val['TCPAlarm']

    def DescribeTCPAlarms(self):
        """ 查看TCP监控

        :returns: 返回TCPAlarmSet，包含TCP监控列表
        """
        val = self.request()
        return val['TCPAlarmSet']

    def DeleteTCPAlarm(self, mid):
        """ 删除TCP监控

        :param mid: 监控项ID
        :type mid: string

        :returns: 请求是否成功
        """
        kwargs = {}
        kwargs['MonitorId'] = mid
        val = self.request(**kwargs)
        return val

    def DisableTCPAlarm(self, mid):
        """ 禁用一个TCP监控项

        :param mid: 监控项ID
        :type mid: string

        :returns: 请求是否成功
        """
        kwargs = {}
        kwargs['MonitorId'] = mid
        val = self.request(**kwargs)
        return val

    def EnableTCPAlarm(self, mid):
        """ 启用一个TCP监控项

        :param mid: 监控项ID
        :type mid: string

        :returns: 请求是否成功
        """
        kwargs = {}
        kwargs['MonitorId'] = mid
        val = self.request(**kwargs)
        return val

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
        :type tid: string
        """

        kwargs = {}
        kwargs['TemplateId'] = tid
        self.request(**kwargs)

    def CreateSecurityGroup(self, name, desc):
        """ 创建安全组

        :param name: 安全组名称
        :type name: string
        :param desc: 安全组描述
        :type desc: string
        """

        kwargs = {}
        kwargs['GroupName'] = name
        kwargs['GroupDescription'] = desc
        val = self.request(**kwargs)
        return val['SecurityGroup']

    def DescribeSecurityGroups(self, ids=None, names=None, limit=0, offset=0,
                               filters=None):
        """ 获取安全组信息

        :param ids: 期望获取的安全组ID列表
        :type ids: list
        :param names: 期望获取的安全组名称列表
        :type names: list
        :param limit: 最多返回数量
        :type limit: int
        :param offset: 返回虚拟机的偏移量，用于分页显示
        :type offset: int
        :param filters: 过滤器，一个dict，包含过滤字段名和值
        :type filters: dict

        """

        kwargs = {}
        if isinstance(ids, list) and len(ids) > 0:
            kwargs['GroupId'] = ids
        if isinstance(names, list) and len(names) > 0:
            kwargs['GroupName'] = names
        self.parse_list_params(limit, offset, filters, kwargs)
        val = self.request(**kwargs)
        return val['SecurityGroupSet']

    def DeleteSecurityGroup(self, gid):
        """ 删除一个安全组

        :param gid: 安全组ID
        :type gid: string
         """

        kwargs = {}
        kwargs['GroupId'] = gid
        self.request(**kwargs)

    def AuthorizeSecurityGroupIngress(self, gid, rules=None):
        """ 给一个安全组授权进入流量的规则(10条上限)

        :param gid: 安全组ID
        :type gid: string
        :param rules: 入流量授权规则的列表
        :type names: list

        规则类型: string
        规则格式: ACTION [IP] PROTOCAL [PORT]
            ACTION: 必填，支持allow/deny
            IP: 选填，默认为0.0.0.0/0，可以是一个IP或一个网段，例如：192.168.0.1，192.168.0.0/16
            PROTOCAL: 必填，支持tcp/udp/icmp/any
            PORT: 选填，如果是any或者是icmp，不必填；如果是tcp或udp，不填时默认为全部端口，填时为指定端口，如8000，
                也支持设定范围，如20-25（注：范围包含的端口个数不能超过30）
        示例:
            'deny tcp 2200'，'deny 192.168.0.0/16 tcp 80'，'allow 192.168.0.0/24 any'，'allow udp 21-22'

        """

        kwargs = {}
        kwargs['GroupId'] = gid
        if rules:
            kwargs['Rule'] = rules
        self.request(**kwargs)

    def RevokeSecurityGroupIngress(self, gid, rules=None):
        """ 从一个安全组中撤销进入流量的规则(指定撤销的规则必须和之前授权的规则完全匹配)

        :param gid: 安全组ID
        :type gid: string
        :param rules: 需要撤销的入流量规则的列表
        :type rules: list

        规则类型: string
        规则格式: 见AuthorizeSecurityGroupIngress

        """

        kwargs = {}
        kwargs['GroupId'] = gid
        if rules:
            kwargs['Rule'] = rules
        self.request(**kwargs)

    def InstanceAssignSecurityGroup(self, iid, gid):
        """ 给一个虚拟机分配安全组

        :param iid: 虚拟机ID
        :type iid: string
        :param gid: 安全组ID
        :type gid: string

        """

        kwargs = {}
        kwargs['InstanceId'] = iid
        kwargs['GroupId'] = gid
        self.request(**kwargs)

    def InstanceRevokeSecurityGroup(self, iid):
        """ 撤销一个虚拟机的安全组

        :param iid: 虚拟机ID
        :type iid: string

        """

        kwargs = {}
        kwargs['InstanceId'] = iid
        self.request(**kwargs)

    def DescribeAvailabilityZones(self, limit=0, offset=0, filters=None):
        """ 获取Zone（可用区）

        :param limit: 返回Zone数量的上限（可选）
        :type limit: int
        :param offset: 返回Zone数量的偏移量，用于分页显示（可选）
        :type offset: int
        :param filters: 过滤条件，key/value分别指定过滤字段名称和值，支持的字段名称为：name，status（可选）
        :type filters: dict

        :returns: AvailabilityZoneSet，包含系统支持的Zone列表
        """
        kwargs = {}
        self.parse_list_params(limit, offset, filters, kwargs)
        val = self.request(**kwargs)
        return val['AvailabilityZoneSet']

    def DescribeRedis(self, ids=None, names=None, limit=0, offset=0,
                                filters=None):
        """ 获得所有Redis

        :param ids: 期望获取的RedisID列表
        :type ids: list
        :param names: 期望获取信息的Redis名称列表
        :type names: list
        :param limit: 最多返回数量
        :type limit: int
        :param offset: 返回Redis的偏移量，用于分页显示
        :type offset: int
        :param filters: 过滤器，一个dict，包含过滤字段名和值，可能过滤字段为：name, status
        :type filters: dict

        :returns: RedisSet，包含Redis列表
        """
        kwargs = {}
        if isinstance(ids, list) and len(ids) > 0:
            kwargs['RedisId'] = ids
        if isinstance(names, list) and len(names) > 0:
            kwargs['RedisName'] = names
        self.parse_list_params(limit, offset, filters, kwargs)
        val = self.request(**kwargs)
        return val['RedisSet']

    def CreateRedis(self, memory, duration=None, name=None, zone=None):
        """ 创建Redis

        :param memory: Redis的内存大小(GB)
        :type memory: int
        :param duration: Redis租期, 缺省为'1M'，即一个月
        :type duration: string
        :param name: Redis名称(可选)
        :type name: string
        :param zone: 可用区，可通过DescribeAvailabilityZones方法查询（可选）
        :type zone: string

        :returns: 创建成功的Redis信息
        """
        kwargs = {}
        kwargs['Memory'] = memory
        if duration is not None:
            if match_duration(duration):
                kwargs['Duration'] = duration
            else:
                raise Exception('Illegal duration format')
        if name is not None:
            kwargs['RedisName'] = name
        if zone is not None:
            kwargs['AvailabilityZoneId'] = zone
        val = self.request(**kwargs)
        return val['Redis']

    def TerminateRedis(self, rid):
        """ 删除Redis

        :param rid: Redis ID
        :type rid: string
        """
        kwargs = {}
        kwargs['RedisId'] = rid
        self.request(**kwargs)

    def RenewRedis(self, rid, duration=None):
        """ Redis租期续费

        :param rid: Redis ID
        :type rid: string
        :param duration: 续费租期，缺省为'1M'，即一个月
        :type duration: string
        """
        kwargs = {}
        kwargs['RedisId'] = rid
        if duration is not None:
            if match_duration(duration):
                kwargs['Duration'] = duration
            else:
                raise Exception('Illegal duration %s' % duration)
        self.request(**kwargs)

    def GetRedisContractInfo(self, rid):
        """ 获取Redis的租期信息

        :param rid: Redis ID
        :type rid: string

        :returns: Redis租期信息，包含过期时间、自动删除时间
        """
        kwargs = {}
        kwargs['RedisId'] = rid
        return self.request(**kwargs)

    def ChangeRedisType(self, rid, memory, duration=None):
        """ 更改Redis类型

        :param rid: Redis ID
        :type rid: string
        :param memory: 指定更改的Redis内存大小，单位GB
        :type memory: int
        :param duration: 指定更改后的初始租期，缺省为'1M'，即一个月
        :type duration: string

        """
        kwargs = {}
        kwargs['RedisId'] = rid
        kwargs['Memory'] = memory
        if duration is not None:
            if match_duration(duration):
                kwargs['Duration'] = duration
            else:
                raise Exception('IIlegal duration format')

        self.request(**kwargs)

    def CreateRedisAlarm(self, rid, metric, operator, threshold, description=None):
        """ 创建Redis指标监控

        :param rid: Redis的ID
        :type rid: string
        :param metric: 监控指标名称
        :type metric: string
        :param operator: 判断操作符
        :type operator: string
        :param threshold: 监控阈值
        :type threshold: string
        :param description: 描述
        :type description: string

        :returns: 请求是否成功
        """
        kwargs = {}
        kwargs['RedisId'] = rid
        kwargs['Metric'] = metric
        kwargs['Operator'] = operator
        kwargs['Threshold'] = threshold
        if description:
            kwargs['Description'] = description
        val = self.request(**kwargs)
        return val['RedisAlarm']

    def DescribeRedisAlarms(self):
        """ 查看Redis指标监控

        :returns: MetricAlarmSet，指标监控列表
        """
        val = self.request()
        return val['RedisAlarmSet']

    def DeleteRedisAlarm(self, mid):
        """ 删除一个Redis指标监控项

        :param mid: 监控项ID
        :type mid: string

        :returns: 请求是否成功
        """
        kwargs = {}
        kwargs['MonitorId'] = mid
        val = self.request(**kwargs)
        return val

    def DisableRedisAlarm(self, mid):
        """ 禁用一个Redis指标监控项

        :param mid: 监控项ID
        :type mid: string

        :returns: 请求是否成功
        """
        kwargs = {}
        kwargs['MonitorId'] = mid
        val = self.request(**kwargs)
        return val

    def EnableRedisAlarm(self, mid):
        """ 启用一个Redis指标监控项

        :param mid: 监控项ID
        :type mid: string

        :returns: 请求是否成功
        """
        kwargs = {}
        kwargs['MonitorId'] = mid
        val = self.request(**kwargs)
        return val

    def DescribeRedisMetrics(self, rid=None):
        """ 查看Redis监控项

        :param rid: Redis ID
        :type rid: string

        :returns: MetricSet，包含监控项列表
        """
        kwargs = {}
        if rid:
            kwargs['RedisId'] = rid
        val = self.request(**kwargs)
        return val['MetricSet']

    def CreateRDS(self, rtype, datadisk, engine, username, password, name, zone, duration=None, **param):
        """ 创建RDS

        :param rtype: RDS类型ID，可通过DescribeRDSTypes方法查询
        :type rtype: string
        :param datadisk: RDS使用的数据盘大小，单位为GB
        :type datadisk: int
        :param engine: RDS的引擎名称，可通过DescribeRDSEngines方法查询
        :type engine: string
        :param username: RDS的用户名
        :type username: string
        :param password: RDS的用户密码
        :type password: string
        :param name: RDS的名称
        :type name: string
        :param zone: 可用区，可通过DescribeAvailabilityZones方法查询
        :type zone: string
        :param duration: RDS租期，单位：'H'(小时)、'M'(月)，缺省为'1M'，即一个月（可选）
        :type duration: string

        :returns: 创建成功的RDS信息
        """
        kwargs = {}
        kwargs['RDSType'] = rtype
        kwargs['ExtraExtDisksize'] = datadisk
        kwargs['Engine'] = engine
        kwargs['RDSUsername'] = username
        kwargs['RDSPassword'] = password
        kwargs['RDSName'] = name

        if zone:
            kwargs['AvailabilityZoneId'] = zone
        if param.get('slave_count'):
            kwargs['SlaveCount'] = param.get('slave_count')
        if param.get('proxy_count'):
            kwargs['ProxyCount'] = param.get('proxy_count', 0)

        if duration is not None:
            if match_duration(duration):
                kwargs['Duration'] = duration
            else:
                raise Exception('Illegal duration format')
        val = self.request(**kwargs)
        return val['RDS']

    def DescribeRDS(self, ids=None, names=None, limit=0, offset=0, filters=None, zone=None):
        """ 获取所有RDS

        :param ids: 期望获取的RDS ID列表（可选）
        :type ids: list
        :param names: 期望获取的RDS名称列表（可选）
        :type names: list
        :param limit: 最多返回数量（可选）
        :type limit: int
        :param offset: 返回RDS的偏移量，用于分页显示（可选）
        :type offset: int
        :param filters: 过滤条件，key/value分别指定过滤字段名称和值，支持的字段名称为：name，status（可选）
        :type filters: dict

        :returns: RDSSet, 包含RDS列表
        """
        kwargs = {}
        if isinstance(ids, list) and len(ids) > 0:
            kwargs['RDSIds'] = ids
        if isinstance(names, list) and len(names) > 0:
            kwargs['RDSNames'] = names
        self.parse_list_params(limit, offset, filters, kwargs)
        if zone:
            kwargs['AvailabilityZoneId'] = zone
        val = self.request(**kwargs)
        return val['RDSSet']

    def StartRDS(self, rid):
        """ 启动RDS

        :param rid: RDS ID
        :type rid: string
        """
        kwargs = {}
        kwargs['RDSId'] = rid
        self.request(**kwargs)

    def StopRDS(self, rid, force=False):
        """ 停止RDS

        :param rid: RDS ID
        :type rid: string
        :param force: 是否强制停止RDS
        :type param: bool
        """
        kwargs = {}
        kwargs['RDSId'] = rid
        if force:
            kwargs['Force'] = force
        self.request(**kwargs)

    def RestartRDS(self, rid):
        """ 重启RDS

        :param rid: RDS ID
        :type rid: string
        """
        kwargs = {}
        kwargs['RDSId'] = rid
        self.request(**kwargs)

    def TerminateRDS(self, rid):
        """ 删除RDS

        :param rid: RDS ID
        :type rid: string

        """
        kwargs = {}
        kwargs['RDSId'] = rid
        self.request(**kwargs)

    def ChangeRDSType(self, rid, rtype, datadisk=None, duration=None):
        """ 更改RDS类型

        :param rid: RDS ID
        :type rid: string
        :param rtype: 指定更改的RDS类型ID，可通过DescribeRDSTypes方法查询
        :type rtype: string
        :param datadisk: 指定更改的RDS数据盘大小，单位GB（可选）
        :type datadisk: int
        :param duration:  指定更改的RDS租期，单位：'H'(小时)、'M'(月)，缺省为'1M'，即一个月（可选）
        :type duration: string

        """
        kwargs = {}
        kwargs['RDSId'] = rid
        kwargs['RDSType'] = rtype
        if datadisk is not None:
            kwargs['ExtraExtDisksize'] = datadisk
        if duration is not None:
            if match_duration(duration):
                kwargs['Duration'] = duration
            else:
                raise Exception('Illegal duration format')
        self.request(**kwargs)

    def DescribeRDSTypes(self, limit=0, offset=0, filters=None):
        """ 获取所有RDS类型

        :param limit: 最大返回数量（可选）
        :type limit: int
        :param offset: 返回RDS类型的偏移量，用于分页显示（可选）
        :type offset: int
        :param filters: 过滤条件，key/value分别指定过滤字段名称和值，支持的字段名称为：name，status（可选）
        :type filters: dict

        :returns: RDSTypeSet，包含系统支持的RDS类型列表
        """
        kwargs = {}
        self.parse_list_params(limit, offset, filters, kwargs)
        val = self.request(**kwargs)
        return val['RDSTypeSet']

    def DescribeRDSEngines(self):
        """ 获取所有RDS引擎

        :returns: RDSEngineSet，包含系统支持的RDS引擎列表
        """
        kwargs = {}
        val = self.request(**kwargs)
        return val['RDSEngineSet']

    def RenewRDS(self, rid, duration=None):
        """ RDS租期续费

        :param rid: RDS ID
        :type rid: string
        :param duration: 续费周期，单位：'H'(小时)、'M'(月)，缺省为'1M'，即一个月（可选）
        :type duration: string

        """
        kwargs = {}
        kwargs['RDSId'] = rid
        if duration is not None:
            if match_duration(duration):
                kwargs['Duration'] = duration
            else:
                raise Exception('Illegal duration format')
        self.request(**kwargs)

    def GetRDSContractInfo(self, rid):
        """ 获取RDS的租期信息

        :param rid: RDS ID
        :type rid: string

        :returns: RDS租期信息，包含过期时间、自动删除时间
        """
        kwargs = {}
        kwargs['RDSId'] = rid
        return self.request(**kwargs)

    def CreateRDSAlarm(self, rid, metric, operator, threshold, description=None):
        """ 创建RDS指标监控

        :param rid: RDS的ID
        :type rid: string
        :param metric: 监控指标名称
        :type metric: string
        :param operator: 判断操作符
        :type operator: string
        :param threshold: 监控阈值
        :type threshold: string
        :param description: 描述
        :type description: string

        :returns: 请求是否成功
        """
        kwargs = {}
        kwargs['RDSId'] = rid
        kwargs['Metric'] = metric
        kwargs['Operator'] = operator
        kwargs['Threshold'] = threshold
        if description:
            kwargs['Description'] = description
        val = self.request(**kwargs)
        return val['RDSAlarm']

    def DescribeRDSAlarms(self):
        """ 查看RDS指标监控

        :returns: MetricAlarmSet，指标监控列表
        """
        val = self.request()
        return val['RDSAlarmSet']

    def DeleteRDSAlarm(self, mid):
        """ 删除一个RDS指标监控项

        :param mid: 监控项ID
        :type mid: string

        :returns: 请求是否成功
        """
        kwargs = {}
        kwargs['MonitorId'] = mid
        val = self.request(**kwargs)
        return val

    def DisableRDSAlarm(self, mid):
        """ 禁用一个RDS指标监控项

        :param mid: 监控项ID
        :type mid: string

        :returns: 请求是否成功
        """
        kwargs = {}
        kwargs['MonitorId'] = mid
        val = self.request(**kwargs)
        return val

    def EnableRDSAlarm(self, mid):
        """ 启用一个RDS指标监控项

        :param mid: 监控项ID
        :type mid: string

        :returns: 请求是否成功
        """
        kwargs = {}
        kwargs['MonitorId'] = mid
        val = self.request(**kwargs)
        return val

    def DescribeRDSMetrics(self, rid=None):
        """ 查看RDS监控项

        :param rid: RDS ID
        :type rid: string

        :returns: MetricSet，包含监控项列表
        """
        kwargs = {}
        if rid:
            kwargs['RDSId'] = rid
        val = self.request(**kwargs)
        return val['MetricSet']

    def CreateVPC(self, name, cidr, desc=None):
        """ 新建VPC

        :param name: VPC名称
        :type name: string
        :param cidr: 选择网段,choose from '10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16'
        :type cidr: string
        :param desc: 描述
        :type desc: string
        :return: VPC实例
        """
        kwargs = dict()
        kwargs['Name'] = name
        kwargs['Cidr'] = cidr
        if desc and not desc.isspace():
            kwargs['Description'] = desc
        val = self.request(**kwargs)  # 利用sys._getframe(level).f_code.co_name获取动态运行时的函数名, 在ec2/action目录下
        return val

    def DeleteVPC(self, vid):
        """删除VPC

        :param vpc_id: VPC ID
        :type vpc_id: string
        :return: 请求是否成功
        """
        kwargs = {'VPCId': vid}
        val = self.request(**kwargs)
        return val

    def UpdateVPC(self, vid, name, desc=None):
        """更新VPC

        :param vpc_id: VPC ID
        :type vpc_id: string
        :param name: VPC名称
        :type name: string
        :param desc: VPC描述
        :type desc: string
        :return: 返回VPC实例
        """
        kwargs = dict()
        kwargs['VPCId'] = vid
        kwargs['Name'] = name
        if desc and not desc.isspace():
            kwargs['Description'] = desc
        val = self.request(**kwargs)  # 利用sys._getframe(level).f_code.co_name获取动态运行时的函数名, 在ec2/action目录下
        return val

    def DescribeVPCs(self, vids=None, limit=0, offset=0, filters=None, zone=None):
        """返回所有或部分VPC信息列表
        :param vids: VPC ID列表
        :type vids: string
        :param limit: 返回数量
        :type limit: string
        :param offset: 偏移
        :type offset: string
        :param filters: 过滤条件
        :type filters: dict
        :param zone: 可用区
        :type zone: string
        :return: VPC实例集合
        """
        kwargs = dict()
        if isinstance(vids, list) and len(vids) > 0:
            kwargs['VPCId'] = vids
        if zone is not None:
            kwargs['AvailabilityZoneId'] = zone
        self.parse_list_params(limit, offset, filters, kwargs)
        val = self.request(**kwargs)
        return val['VPCSet']

    def CreateVPCSubnet(self, name, vpcid, zoneid, startip, endip, netmask, gateway, desc=None):
        """创建子网

        :param name: VPC名称
        :type name: string
        :param vpcid: VPC ID
        :type vpcid: string
        :param zoneid: 可用区ID
        :type zoneid: string
        :param startip: 子网起始IP
        :type startip: string
        :param endip: 子网结束IP
        :type endip: string
        :param netmask: 子网掩码
        :type netmask: string
        :param desc: 描述
        :type desc: string
        :return: 子网实例
        """
        kwargs = dict()
        kwargs['Name'] = name
        kwargs['VPCId'] = vpcid
        kwargs['StartIp'] = startip
        kwargs['EndIp'] = endip
        kwargs['NetMask'] = netmask
        kwargs['Gateway'] = gateway
        if zoneid:
            kwargs['AvailabilityZoneId'] = zoneid
        if desc and not desc.isspace():
            kwargs['Description'] = desc
        val = self.request(**kwargs)
        return val

    def DeleteVPCSubnet(self, subnetid):
        """删除子网
        :param subnetid: 子网ID
        :type subnetid: string
        :return: 请求是否成功
        """
        kwargs = dict()
        kwargs['SubnetId'] = subnetid
        val = self.request(**kwargs)
        return val

    def UpdateVPCSubnet(self, subnetid, name, desc=None):
        """更新子网

        :param subnetid: 子网ID
        :type subnetid: string
        :param name: 名称
        :type name: string
        :param desc: 描述
        :type desc: string
        :return: 子网实例
        """
        kwargs = dict()
        kwargs['SubnetId'] = subnetid
        kwargs['Name'] = name
        if desc and not desc.isspace():
            kwargs['Description'] = desc
        val = self.request(**kwargs)
        return val

    def DescribeVPCSubnets(self, subnets_ids=None, limit=0, offset=0, filters=None, zone=None):
        """ 返回所有或部分子网信息列表
        :param subnets_ids: 子网ID列表
        :type subnets_ids: list
        :param limit: 返回数量
        :type limit: string
        :param offset: 偏移
        :type offset: string
        :param filters: 过滤条件
        :type filters: dict
        :param zone: 可用区
        :type zone: string
        :return: 子网实例集合
        """
        kwargs = dict()
        if isinstance(subnets_ids, list) and len(subnets_ids) > 0:
            kwargs['SubnetId'] = subnets_ids
        if zone is not None:
            kwargs['AvailabilityZoneId'] = zone
        self.parse_list_params(limit, offset, filters, kwargs)
        val = self.request(**kwargs)
        return val['SubnetSet']

    def ListVPCSubnets(self, vpc_id, limit=0, offset=0, filters=None):
        """列出VPC下所有子网列表

        :param vpc_id: VPC ID
        :type vpc_id: string
        :param limit: 返回数量
        :type limit: string
        :param offset: 偏移
        :type offset: string
        :param filters: 过滤条件
        :type filters: dict
        :return: 子网实例集合
        """
        kwargs = dict()
        kwargs["VPCId"] = vpc_id
        self.parse_list_params(limit, offset, filters, kwargs)
        val = self.request(**kwargs)
        return val['SubnetSet']

    def AllocateAddress(self, name, billing_model='bandwidth', availability_zone_id=None):
        """ 分配浮动IP

        :param name:
        :param billing_model: 代表计费方式，有效值：bandwidth，flow，分别代表按带宽和按流量计费。默认为bandwidth
        :param availability_zone_id: 代表可用区ID, 通过DescribeAvailabilityZones接口获取
        :return: Address结构
        """
        kwargs = dict()
        kwargs['Name'] = name
        kwargs['BillingModel'] = billing_model
        if availability_zone_id:
            kwargs['AvailabilityZoneId'] = availability_zone_id
        val = self.request(**kwargs)
        return val

    def DescribeAddresses(self, allocation_ids=None, limit=0, offset=0, filters=None, zone=None):
        """ 返回所有或者部分浮动IP列表信息列表

        :param allocation_ids:  希望获取的Address ID列表
        :type allocation_ids: list
        :param limit: 返回的数量限制，用于分页控制
        :type limit: int
        :param offset: 返回的偏移量，用于分页控制
        :type offset: int
        :param filters: 过滤器，一个dict，包含过滤字段名和值
        :type filters: dict
        :return: AddressSet, 包含Address列表
        """
        kwargs = dict()
        if isinstance(allocation_ids, list) and len(allocation_ids) > 0:
            kwargs['AllocationId'] = allocation_ids
        if zone is not None:
            kwargs['AvailabilityZoneId'] = zone
        self.parse_list_params(limit, offset, filters, kwargs)
        val = self.request(**kwargs)
        return val['AddressSet']

    def ConfigAddress(self, allocation_id, name=None):
        """ 配置浮动IP, 目前支持名称修改

        :param allocation_id: 浮动IP的ID（或者IP）
        :param name: 浮动IP的名称
        :return: Address结构
        """
        kwargs = {'AllocationId': allocation_id}
        if name:
            kwargs['Name'] = name
        val = self.request(**kwargs)
        return val

    def ConfigAddressBandwidth(self, allocation_id, bandwidth=None):
        """ 配置浮动IP带宽

        :param allocation_id: 浮动IP的ID（或者IP）
        :param bandwidth: 浮动IP的带宽
        :return: Address结构
        """
        kwargs = {'AllocationId': allocation_id}
        if bandwidth:
            kwargs['Bandwidth'] = bandwidth
        val = self.request(**kwargs)
        return val['Address']

    def ReleaseAddress(self, allocation_id):
        """ 释放浮动IP

        :param allocation_id: 浮动IP的ID（或者IP）
        :return: 请求是否成功
        """
        kwargs = {'AllocationId': allocation_id}
        val = self.request(**kwargs)
        return val

    def AssociateAddress(self, allocation_id, association_type, instance_id, bandwidth):
        """ 将浮动IP绑定到其他云产品上

        :param allocation_id: 浮动IP的ID（或者IP）
        :param association_type: 绑定云产品类型。有效值为server、elb，分别代表绑定到云服务器和ELB负载均衡器
        :param instance_id: 绑定的云产品ID
        :param bandwidth: 绑定浮动IP的带宽限制
        :return: Address结构
        """
        kwargs = {'AllocationId': allocation_id, 'AssociationType': association_type,
                  'InstanceId': instance_id, 'Bandwidth': bandwidth}
        val = self.request(**kwargs)
        return val

    def DisassociateAddress(self, allocation_id):
        """ 将浮动IP解绑

        :param allocation_id: 浮动IP的ID（或者IP）
        :return: 请求是否成功
        """
        kwargs = {'AllocationId': allocation_id}
        val = self.request(**kwargs)
        return val

    def ReplaceAddress(self, allocation_id, new_allocation_id, sync=False, timeout=300):
        """ 将浮动IP换绑

        :param allocation_id: 浮动IP的ID（或者IP）
        :param new_allocation_id: 新的浮动IP的ID（或者IP）
        :return: Address结构
        """
        kwargs = {
            'AllocationId': allocation_id,
            'NewAllocationId': new_allocation_id,
            'Sync': sync,
            'Timeout': timeout,
        }
        val = self.request(**kwargs)
        return val

    ##
    #   EBS code
    #
    def CreateVolume(self, name, disksize, zone=None):
        """ 创建EBS

        :param name: EBS 的name
        :type name: string
        :param disksize: EBS 的大小 单位G
        :type disksize: string
        :param zone: 可用区，可通过DescribeAvailabilityZones方法查询（可选）
        :type zone: string

        :return: Volume, 包含Volume结构列表
        """
        kwargs = {}
        kwargs['Size'] = disksize
        if name is not None:
            kwargs['VolumeName'] = name
        if zone is not None:
            kwargs['AvailabilityZoneId'] = zone
        val = self.request(**kwargs)
        return val

    def DescribeVolumes(self, ebs_ids=None, zone=None, limit=0, offset=0, filters=None):
        """ 获取EBS实例列表
        :param ebs_ids:  EBS ID列表
        :type ebs_ids: list
        :param limit:
        :type limit: int
        :param offset:
        :type offset: int
        :param filters:
        :type filters: dict
        :returns: VolumeSet, 包含Volume结构列表
        """
        kwargs = dict()
        if isinstance(ebs_ids, list) and len(ebs_ids) > 0:
            kwargs['VolumeIds'] = ebs_ids
        if zone is not None:
            kwargs['AvailabilityZoneId'] = zone
        self.parse_list_params(limit, offset, filters, kwargs)
        val = self.request(**kwargs)
        return val['VolumeSet']

    def AttachVolume(self, ebs_id, instance_id):
        """ 绑定EBS 到 实例

        :param instance_id: 实例的ID
        :param ebs_id: EBS的ID
        :return: 请求是否成功
        """
        kwargs = {'InstanceId': instance_id, 'VolumeId': ebs_id}
        val = self.request(**kwargs)
        return val

    def DetachVolume(self, ebs_id, instance_id):
        """ 卸载EBS

        :param ebs_id: EBS的ID
        :return: 请求是否成功
        """
        kwargs = {'VolumeId': ebs_id, 'InstanceId': instance_id}
        val = self.request(**kwargs)
        return val

    def DeleteVolume(self, ebs_id):
        """ 删除EBS

        :param ebs_id: EBS的ID
        :return: 请求是否成功
        """
        kwargs = {'VolumeId': ebs_id}
        val = self.request(**kwargs)
        return val

    def DescribeVolumeSnapshots(self, ebs_snapshot_ids=None, zone=None, limit=0, offset=0, filters=None):
        """ 获取EBS快照实例列表
        :param ebs_snapshot_ids:  EBS ID列表
        :type ebs_snapshot_ids: list
        :param limit:
        :type limit: int
        :param offset:
        :type offset: int
        :param filters:
        :type filters: dict
        :return: VolumeSnapshotSet, 包含VolumeSnapshot结构列表
        """
        kwargs = dict()
        if isinstance(ebs_snapshot_ids, list) and len(ebs_snapshot_ids) > 0:
            kwargs['VolumeSnapshotIds'] = ebs_snapshot_ids
        if zone is not None:
            kwargs['AvailabilityZoneId'] = zone

        self.parse_list_params(limit, offset, filters, kwargs)
        val = self.request(**kwargs)
        return val['VolumeSnapshotSet']

    def CreateVolumeSnapshot(self, name, ebs_id):
        """ 创建EBS快照

        :param name: 快照的名称
        :param ebs_id: EBS的ID
        :return: 请求是否成功
        """
        kwargs = {'VolumeSnapshotName': name, 'VolumeId': ebs_id}
        val = self.request(**kwargs)
        return val

    def RecoverVolume(self, ebs_snapshot_id):
        """ 用快照恢复EBS

        :param ebs_snapshot_id: EBS快照的ID
        :return: 请求是否成功
        """
        kwargs = {'VolumeSnapshotId': ebs_snapshot_id}
        val = self.request(**kwargs)
        return val

    def DeleteVolumeSnapshot(self, ebs_snapshot_id):
        """ 删除EBS快照

        :param ebs_snapshot_id: EBS快照的ID
        :return: 请求是否成功
        """
        kwargs = {'VolumeSnapshotId': ebs_snapshot_id}
        val = self.request(**kwargs)
        return val

    """
        主机分组
    """
    def DescribeServerGroup(self, servergroup_ids=None, zone=None, limit=0, offset=0, filters=None):
        """ 获取分组列表
        :param servergroup_ids:  分组 ID列表
        :type servergroup_ids: list
        :param limit:
        :type limit: int
        :param offset:
        :type offset: int
        :param filters:
        :type filters: dict
        :return: ServerGroupSet, 包含ServerGroup结构列表
        """
        kwargs = dict()
        if isinstance(servergroup_ids, list) and len(servergroup_ids) > 0:
            kwargs['ServerGroupIds'] = servergroup_ids
        if zone is not None:
            kwargs['AvailabilityZoneId'] = zone

        self.parse_list_params(limit, offset, filters, kwargs)
        val = self.request(**kwargs)
        return val['ServerGroupSet']

    def CreateServerGroup(self, name, zone=None):
        """ 创建分组
        :param name: 分组 Name
        :type name:string
        :param zone: 分区 ID or Name
        :type zone: string
        :return: ServerGroup结构列表

        """
        kwargs = {}
        kwargs['Name'] = name
        if zone is not None:
            kwargs['AvailabilityZoneId'] = zone

        val = self.request(**kwargs)
        return val

    def ReleaseServerGroup(self, group):
        """ 删除分组
        :param group: 分组 名称 or ID
        :type grop: string
        :return: return
        """

        kwargs = {}
        kwargs['Group'] = group
        val = self.request(**kwargs)
        return val

    # def ServerGroupShow(self, instance_id, zone=None):

    #     kwargs = {}
    #     kwargs['InstanceId'] = instance_id
    #     val = self.request(**kwargs)
    #     return val

    def DescribeServerByGroup(self, group=None, zone=None, limit=0, offset=0, filters=None):
        """ 分组内机器资源列表
        :param group: 分组 名称 or ID
        :type grop: string
        :return: GroupGuestSet, 包含GroupGuest结构列表
        """

        kwargs = {}
        if group:
            kwargs['Group'] = group
        if zone is not None:
            kwargs['AvailabilityZoneId'] = zone
        self.parse_list_params(limit, offset, filters, kwargs)
        val = self.request(**kwargs)
        return val['GroupGuestSet']

    def ServerJoinGroup(self, group, instance_id, tag=None):
        """ 添加实例到指定分组
        :param group: 分组 名称 or ID
        :type grop: string
        :param instance_id: InstanceId 对应的实例资源
        :type instance_id: string
        :return: GroupGuest结构列表
        """

        kwargs = {}
        kwargs['Group'] = group
        kwargs['InstanceId'] = instance_id
        if tag:
            kwargs['Tag'] = tag
        val = self.request(**kwargs)
        return val

    def ServerLeaveGroup(self, group, instance_id):
        """ 将实例从分组里面移除
        :param group: 分组 名称 or ID
        :type grop: string
        :param instance_id: InstanceId 对应的实例资源
        :type instance_id: string
        :return: return
        """

        kwargs = {}
        kwargs['Group'] = group
        kwargs['InstanceId'] = instance_id
        val = self.request(**kwargs)
        return val

    """
        ECS API
    """
    def DescribeECS(self, ecs_ids=None, zone=None, limit=None, offset=None, filters=None):
        """ 获取EBS实例列表
        :param ecs_ids:  ECS ID列表
        :type ecs_ids: list
        :param limit:
        :type limit: int
        :param offset:
        :type offset: int
        :param filters:
        :type filters: dict
        :returns: ECSSet, 包含ECS结构列表
        """
        kwargs = dict()
        if isinstance(ecs_ids, list) and len(ecs_ids) > 0:
            kwargs['ECSIds'] = ecs_ids
        if zone is not None:
            kwargs['AvailabilityZoneId'] = zone
        self.parse_list_params(limit, offset, filters, kwargs)
        val = self.request(**kwargs)
        return val['ECSSet']

    def CreateECS(self, name, flavor , driver, master_count=1, zone=None):
        """ 创建ECS
        :param name: ECS Name
        :type name:string
        :param flavor: ECS 类型
        :type flavor: string
        :param driver: ECS driver
        :type driver: string
        :param master_count: 主节点数
        :type master_count: int
        :param zone: 分区 ID or Name
        :type zone: string
        :return: ECS结构列表

        """
        kwargs = {}
        kwargs['Name'] = name
        kwargs['ECSType'] = flavor
        kwargs['Driver'] = driver
        if master_count:
            kwargs['MasterCount'] = master_count
        if zone is not None:
            kwargs['AvailabilityZoneId'] = zone

        val = self.request(**kwargs)
        return val

    def ChangeECSType(self, ecs_id, flavor):
        """ 更改ECS 配置
        :param ecs_id: ECS ID
        :type ecs_id:string
        :param flavor: ECS 类型
        :type flavor: string
        :return: return

        """
        kwargs = {}
        kwargs['ECSId'] = ecs_id
        kwargs['ECSType'] = flavor

        val = self.request(**kwargs)
        return val

    def DeleteECS(self, ecs_id):
        """ 删除ECS
        :param ecs_id: ECS ID
        :type ecs_id:string
        :return: ECS结构列表

        """
        kwargs = {}
        kwargs['ECSId'] = ecs_id

        val = self.request(**kwargs)
        return val

    def DescribeECSNode(self, ecs, limit=None, offset=None, filters=None):
        """ ECS Node 列表
        :param ecs_id: ECS ID
        :type ecs_id:string
        :param limit:
        :type limit: int
        :param offset:
        :type offset: int
        :param filters:
        :type filters: dict
        :return: ECS结构列表

        """
        kwargs = {}
        kwargs['ECSId'] = ecs
        self.parse_list_params(limit, offset, filters, kwargs)

        val = self.request(**kwargs)
        return val['RDSNodeSet']

    def CreateECSNode(self, ecs_id, count):
        """ 创建ECS Node
        :param ecs_id: ECS ID
        :type ecs_id:string
        :return: ECS结构列表

        """
        kwargs = {}
        kwargs['ECSId'] = ecs_id
        if count:
            kwargs['Count'] = count

        val = self.request(**kwargs)
        return val

    def DeleteCDSNode(self, node_id):
        """ 删除CDS Node
        :param node_id: Node ID
        :type node_id:string
        :return: ECS结构列表

        """
        kwargs = {}
        kwargs['NodeId'] = node_id

        val = self.request(**kwargs)
        return val

    def DescribeRDSNode(self, rds, limit=None, offset=None, filters=None):
        """ RDS Node 列表
        :param rds: RDS ID
        :type rds:string
        :param limit:
        :type limit: int
        :param offset:
        :type offset: int
        :param filters:
        :type filters: dict
        :return: ECS结构列表

        """
        kwargs = {}
        kwargs['RDSId'] = rds
        self.parse_list_params(limit, offset, filters, kwargs)

        val = self.request(**kwargs)
        return val['RDSNodeSet']

    def CreateRDSNode(self, rds_id, role, count):
        """ 创建RDS Node
        :param rds_id: ECS ID
        :type rds_id:string
        :return: ECS结构列表

        """
        kwargs = {}
        kwargs['RDSId'] = rds_id
        kwargs['Role'] = role
        if count:
            kwargs['Count'] = count

        val = self.request(**kwargs)
        return val

    """
        BigData API
    """
    def DescribeSDSystems(self, ids=None, names=None, zone=None, filters=None,
                          limit=10, offset=0, order_by='id', order='asc'):
        u"""获取实时计算集群列表信息.

        :param ids: 期望获取的StreamingSystemID列表
        :type ids: list
        :param names: 期望获取信息的StreamingSystem名称列表
        :type names: list
        :param zone: 指定创建StreamingSystem所在的数据中心
        :type zone: string
        :param limit: 最多返回数量
        :type limit: int
        :param offset: 返回StreamingSystem的偏移量，用于分页显示
        :type offset: int
        :param filters: 过滤器，一个dict，包含过滤字段名和值，可能过滤字段为：name, status
        :type filters: dict
        :param order_by: 排序字段
        :type order_by: string
        :param order: 值只能为'desc'(升序)或者'asc'(降序)
        :type order: string

        :returns: StreamingSystemSet，包含StreamingSystem列表
        """
        kwargs = {}
        if isinstance(ids, list) and len(ids) > 0:
            kwargs['StreamingSystemIds'] = ids
        if isinstance(names, list) and len(names) > 0:
            kwargs['SteamingSystemNames'] = names
        if zone is not None:
            kwargs['ZoneId'] = zone
        if order_by and order:
            kwargs['OrderBy'] = order_by
            kwargs['Order'] = order
        self.parse_list_params(limit, offset, filters, kwargs)
        val = self.request(**kwargs)
        return val['StreamingSystemSet']

    def DescribeBDSystems(self, ids=None, names=None, zone=None, filters=None,
                          limit=10, offset=0, order_by='id', order='asc'):
        u"""获取所有Hadoop集群集群列表信息.

        :param ids: 期望获取的BigDataSystemID列表
        :type ids: list
        :param names: 期望获取信息的BigDataSystem名称列表
        :type names: list
        :param zone: 指定创建BigDataSystem所在的数据中心名称
        :type zone: string
        :param limit: 最多返回数量
        :type limit: int
        :param offset: 返回BigDataSystem的偏移量，用于分页显示
        :type offset: int
        :param filters: 过滤器，一个dict，包含过滤字段名和值，可能过滤字段为：name, status
        :type filters: dict
        :param order_by: 排序字段
        :type order_by: string
        :param order: 值只能为'desc'(升序)或者'asc'(降序)
        :type order: string

        :returns: BigDataSystemSet，包含BigDataSystem列表
        """
        kwargs = {}
        if isinstance(ids, list) and len(ids) > 0:
            kwargs['BigDataSystemIds'] = ids
        if isinstance(names, list) and len(names) > 0:
            kwargs['BigDataSystemNames'] = names
        if zone is not None:
            kwargs['ZoneId'] = zone
        if order_by and order:
            kwargs['OrderBy'] = order_by
            kwargs['Order'] = order
        self.parse_list_params(limit, offset, filters, kwargs)
        val = self.request(**kwargs)
        return val['BigDataSystemSet']

    def StartBDSystem(self, idstr):
        u"""启动集群.

        :param idstr: 集群ID
        :type idstr: string
        :return:
        """
        kwargs = {}
        kwargs['BigDataSystemID'] = idstr
        self.request(**kwargs)

    def StopBDSystem(self, idstr):
        u"""暂停集群.

        :param idstr: 集群ID
        :type idstr: string
        :return:
        """
        kwargs = {}
        kwargs['BigDataSystemID'] = idstr
        self.request(**kwargs)

    def DeleteBDSystem(self, idstr):
        u"""删除集群.

        :param idstr: 集群ID
        :type idstr: string
        :return:
        """
        kwargs = {}
        kwargs['BigDataSystemID'] = idstr
        self.request(**kwargs)

    def ScaleUpBDSystem(self, idstr, delta):
        u"""扩容集群.

        :param idstr: 集群ID
        :type idstr: string
        :param delta: 扩容的nodes数量
        :type delta: int
        :return:
        """
        kwargs = {}
        kwargs['BigDataSystemID'] = idstr
        kwargs['Delta'] = delta
        self.request(**kwargs)

    def ScaleDownBDSystem(self, idstr, delta):
        u"""减容集群.

        :param idstr: 集群ID
        :type idstr: string
        :param delta: 减容的nodes数量
        :type delta: int
        :return:
        """
        kwargs = {}
        kwargs['BigDataSystemID'] = idstr
        kwargs['Delta'] = delta
        self.request(**kwargs)

    def StartSDSystem(self, idstr):
        u"""启动集群.

        :param idstr: 集群ID
        :type idstr: string
        :return:
        """
        kwargs = {}
        kwargs['StreamingSystemID'] = idstr
        self.request(**kwargs)

    def StopSDSystem(self, idstr):
        u"""暂停集群.

        :param idstr: 集群ID
        :type idstr: string
        :return:
        """
        kwargs = {}
        kwargs['StreamingSystemID'] = idstr
        self.request(**kwargs)

    def DeleteSDSystem(self, idstr):
        u"""删除集群.

        :param idstr: 集群ID
        :type idstr: string
        :return:
        """
        kwargs = {}
        kwargs['StreamingSystemID'] = idstr
        self.request(**kwargs)

    def ScaleUpSDSystem(self, idstr, delta):
        u"""扩容集群.

        :param idstr: 集群ID
        :type idstr: string
        :param delta: 扩容的nodes数量
        :type delta: int
        :return:
        """
        kwargs = {}
        kwargs['StreamingSystemID'] = idstr
        kwargs['Delta'] = delta
        self.request(**kwargs)

    def ScaleDownSDSystem(self, idstr, delta):
        u"""减容集群.

        :param idstr: 集群ID
        :type idstr: string
        :param delta: 减容的nodes数量
        :type delta: int
        :return:
        """
        kwargs = {}
        kwargs['StreamingSystemID'] = idstr
        kwargs['Delta'] = delta
        self.request(**kwargs)

    def CreateBDSystem(self,
                       name, architecture, slave_count, bds_type,
                       zone, admin_pass, description=None):
        u"""创建Hadoop集群.

        :param name: 集群名称
        :type name: string
        :param architecture: 集群架构类型,目前支持'single_master'
        :type architecture: string
        :param slave_count: 集群规模
        :type slave_count: int
        :param bds_type: 集群选用的配置类型，通过DescribeBDSTypes查找
        :type bds_type: string
        :param zone: 可以为zone的name或者id
        :type zone: string
        :param admin_pass: 管理员密码
        :type admin_pass: string
        :param description:
        :type description: string
        :return: BigDataSystem结构
        """
        kwargs = {}
        kwargs['BigDataSystemName'] = name
        kwargs['Architecture'] = architecture
        kwargs['SlaveCount'] = slave_count
        kwargs['BigDataSystemType'] = bds_type
        kwargs['Zone'] = zone
        kwargs['AdminPassword'] = admin_pass
        if description:
            kwargs['Description'] = description
        val = self.request(**kwargs)
        return val['BigDataSystem']

    def CreateSDSystem(self,
                       name, architecture, slave_count,
                       bds_type, zone, admin_pass,
                       description=None):
        u"""创建实时计算集群.

        :param name: 集群名称
        :type name: string
        :param architecture: 集群架构,目前支持'single_master'
        :type architecture: string
        :param slave_count: 集群规模数量
        :type slave_count: int
        :param bds_type: 集群选用的配置类型，通过DescribeSDSTypes查找
        :type bds_type: string
        :param zone: 可以为zone的name或者id
        :type zone: string
        :param admin_pass: 管理员密码
        :type admin_pass: string
        :param description:
        :type description: string
        :return: StreamingSystem结构
        """
        kwargs = {}
        kwargs['StreamingSystemName'] = name
        kwargs['Architecture'] = architecture
        kwargs['SlaveCount'] = slave_count
        kwargs['StreamingSystemType'] = bds_type
        kwargs['Zone'] = zone
        kwargs['AdminPassword'] = admin_pass
        if description:
            kwargs['Description'] = description
        val = self.request(**kwargs)
        return val['StreamingSystem']

    def DescribeBDSTypes(self, limit=0, offset=0, filters=None):
        u"""获取所有BigDataSystem(简称BDS)类型.

        :param limit: 最大返回数量（可选）
        :type limit: int
        :param offset: 返回BDS类型的偏移量，用于分页显示（可选）
        :type offset: int
        :param filters: 过滤条件，key/value分别指定过滤字段名称和值，支持的字段名称为：name，status（可选）
        :type filters: dict
        :returns: BDSTypeSet，包含系统支持的BDS类型列表
        """
        kwargs = {}
        self.parse_list_params(limit, offset, filters, kwargs)
        val = self.request(**kwargs)
        return val['BDSTypeSet']

    def DescribeSDSTypes(self, limit=0, offset=0, filters=None):
        u"""获取所有StreamingSystem(简称SDS)类型.

        :param limit: 最大返回数量（可选）
        :type limit: int
        :param offset: 返回SDS类型的偏移量，用于分页显示（可选）
        :type offset: int
        :param filters: 过滤条件，key/value分别指定过滤字段名称和值，支持的字段名称为：name，status（可选）
        :type filters: dict
        :returns: SDSTypeSet，包含系统支持的SDS类型列表
        """
        kwargs = {}
        self.parse_list_params(limit, offset, filters, kwargs)
        val = self.request(**kwargs)
        return val['SDSTypeSet']

    @utils.expect('LoadBalancer')
    def CreateLoadBalancer(self, name, allocation_id, bandwidth=None, zone=None):
        """ 创建ELB

        :param name: ELB名称
        :type name: string
        :param allocation_id: EIP 浮动IP的AllocationId
        :type allocation_id: string
        :param bandwidth: 指定创建虚拟机使用的额外带宽，单位为Mbps
        :type bandwidth: int
        :param zone: 指定创建虚拟机所在的数据中心, 可通过DescribeAvailabilityZones接口获取
        :type zone: string
        :return: 创建成功的ELB信息
        """
        kwargs = {}
        kwargs['Name'] = name
        kwargs['AllocationId'] = allocation_id
        bandwidth = int(bandwidth)
        if bandwidth <= 0:
            raise Exception('Illegal bandwidth: %d, should larger than 0' % bandwidth)
        kwargs['Bandwidth'] = bandwidth
        if zone is not None:
            kwargs['AvailabilityZoneId'] = zone
        return self.request(**kwargs)

    def DeleteLoadBalancer(self, elb_id):
        """ 删除ELB

        :param elb_id: ELB id
        :type elb_id: string
        :return: 请求是否成功
        """
        kwargs = {'LoadBalancerId': elb_id}
        val = self.request(**kwargs)
        return val

    @utils.expect('LoadBalancerSet')
    def DescribeLoadBalancers(self, ids=None, limit=0, offset=0, filters=None, zone=None):
        """ 获得所有ELB

        :param ids: 期望获取的ELB ID列表
        :type ids: list
        :param limit: 最多返回数量
        :type limit: int
        :param offset: 返回虚拟机的偏移量，用于分页显示
        :type offset: int
        :param filters: 过滤器，一个dict，包含过滤字段名和值，可能过滤字段为：name, status
        :type filters: dict
        :param zone: 指定创建虚拟机所在的数据中心, 可通过DescribeAvailabilityZones接口获取
        :type zone: string

        :returns: LoadBalancerSet，包含ELB列表
        """
        kwargs = {}
        if isinstance(ids, list) and len(ids) > 0:
            kwargs['LoadBalancerId'] = ids
        if zone is not None:
            kwargs['AvailabilityZoneId'] = zone
        self.parse_list_params(limit, offset, filters, kwargs)
        return self.request(**kwargs)

    @utils.expect('LoadBalancer')
    def ModifyLoadBalancerAttributes(self, elb_id, name=None, bandwidth=None, allocation_id=None):
        """ 配置负载均衡 ELB 实例信息
        :param elb_id: ELB id
        :type elb_id: string
        :param name: ELB name
        :type name: string
        :param allocation_id: EIP 浮动IP的AllocationId或者IP
        :type allocation_id: string
        :param bandwidth: 指定创建虚拟机使用的额外带宽，单位为Mbps
        :type bandwidth: int

        :return: LoadBalancer
        """
        kwargs = {}
        kwargs['LoadBalancerId'] = elb_id
        if name is not None:
            kwargs['Name'] = name
        if bandwidth is not None:
            bandwidth = int(bandwidth)
            if bandwidth <= 0:
                raise Exception('Illegal bandwidth: %d, should larger than 0' % bandwidth)
            kwargs['Bandwidth'] = bandwidth
        if allocation_id is not None:
            kwargs['AllocationId'] = allocation_id
        return self.request(**kwargs)

    @utils.expect('Listener')
    def CreateLoadBalancerListener(self, name, alg, protocol, frontend_port,
                                   backend_port, elb_id, enablesessionsticky=False,
                                   check_interval=5, check_rise=None,
                                   check_fall=None, check_timeout=3,
                                   domain=None, location=None,
                                   cookie_name=None, check_url=None,
                                   session_mode=None, session_timeout=None,
                                   certificate_id=None):
        """ 创建ELB 监听转发策略

        :param name: 监听转发策略名称
        :type name: string
        :param alg: 有效值为wrr（加权轮询）、rr（轮询），转发调度策略
        :type alg: string
        :param protocol: 转发协议, 有效值TCP、HTTP、HTTPS
        :type protocol: string
        :param frontend_port: 监听转发规则的对外服务端口
        :type frontend_port: int
        :param backend_port: 监听转发规则到后端服务器池的端口
        :type backend_port: int
        :param enablesessionsticky: 是否打开会话保持
        :type enablesessionsticky: boolean
        :param elb_id: ELB实例的ID
        :type elb_id: string
        :param check_interval: 健康检查时间间隔, 默认5
        :type check_interval: int
        :param check_rise: 连续健康检查成功多少次后，认为后端服务可用
        :type check_rise: int
        :param check_fall: 连续健康检查失败多少次后，认为后端服务不可用
        :type check_fall: int
        :param check_timeout: 健康检查超时时间, 默认3
        :type check_timeout: int
        :param domain: 转发规则对应的域名
        :type domain: string
        :param location: 转发规则对应的URL location
        :type location: string
        :param cookie_name: 指定七层会话保持的cookie名称
        :type cookie_name: string
        :param check_url: 健康检查URL
        :type check_url: string
        :param session_mode: 会话保持模式
        :type session_mode: string
        :param session_timeout: 会话保持超时时间
        :type session_timeout: int
        :param certificate_id: Https类型转发对应的证书ID
        :type certificate_id: string

        :return: 创建成功的监听转发策略
        """
        kwargs = {}
        kwargs['Name'] = name
        kwargs['Alg'] = alg
        kwargs['Protocol'] = protocol
        kwargs['FrontendPort'] = frontend_port
        kwargs['BackendPort'] = backend_port
        kwargs['EnableSessionSticky'] = enablesessionsticky
        kwargs['LoadBalancerId'] = elb_id
        kwargs['CheckInterval'] = check_interval
        if check_rise is not None:
            kwargs['CheckRise'] = check_rise
        if check_fall is not None:
            kwargs['CheckFall'] = check_fall
        kwargs['CheckTimeout'] = check_timeout
        if domain is not None:
            kwargs['Domain'] = domain
        if location is not None:
            kwargs['Location'] = location
        if cookie_name is not None:
            kwargs['CookieName'] = cookie_name
        if check_url is not None:
            kwargs['CheckUrl'] = check_url
        if session_mode is not None:
            kwargs['SessionMode'] = session_mode
        if session_timeout is not None:
            kwargs['SessionTimeout'] = session_timeout
        if certificate_id is not None:
            kwargs['CertificateId'] = certificate_id
        return self.request(**kwargs)

    @utils.expect('Listener')
    def ConfigLoadBalancerListener(self, listenser_id, alg=None, protocol=None,
                                   frontend_port=None, backend_port=None, name=None,
                                   enablesessionsticky=None, check_interval=None,
                                   check_rise=None, check_fall=None,
                                   check_timeout=None, domain=None,
                                   location=None, cookie_name=None,
                                   check_url=None, session_mode=None,
                                   session_timeout=None, certificate_id=None):
        """ 配置指定的监听转发策略

        :param listenser_id: 转发调度策略的ID
        :type listenser_id: string
        :param name: 监听转发策略名称
        :type name: string
        :param alg: 有效值为wrr（加权轮询）、rr（轮询），转发调度策略
        :type alg: string
        :param protocol: 转发协议, 有效值TCP、HTTP、HTTPS
        :type protocol: string
        :param frontend_port: 监听转发规则的对外服务端口
        :type frontend_port: int
        :param backend_port: 监听转发规则到后端服务器池的端口
        :type backend_port: int
        :param enablesessionsticky: 是否打开会话保持
        :type enablesessionsticky: boolean
        :param check_interval: 健康检查时间间隔, 默认5
        :type check_interval: int
        :param check_rise: 连续健康检查成功多少次后，认为后端服务可用
        :type check_rise: int
        :param check_fall: 连续健康检查失败多少次后，认为后端服务不可用
        :type check_fall: int
        :param check_timeout: 健康检查超时时间, 默认3
        :type check_timeout: int
        :param domain: 转发规则对应的域名
        :type domain: string
        :param location: 转发规则对应的URL location
        :type location: string
        :param cookie_name: 指定七层会话保持的cookie名称
        :type cookie_name: string
        :param check_url: 健康检查URL
        :type check_url: string
        :param session_mode: 会话保持模式
        :type session_mode: string
        :param session_timeout: 会话保持超时时间
        :type session_timeout: int
        :param certificate_id: Https类型转发对应的证书ID
        :type certificate_id: string

        :return: 创建成功的监听转发策略
        """
        kwargs = {}
        kwargs['ListenerId'] = listenser_id
        if name is not None:
            kwargs['Name'] = name
        if alg is not None:
            kwargs['Alg'] = alg
        if protocol is not None:
            kwargs['Protocol'] = protocol
        if frontend_port is not None:
            kwargs['FrontendPort'] = frontend_port
        if backend_port is not None:
            kwargs['BackendPort'] = backend_port
        if enablesessionsticky is not None:
            kwargs['EnableSessionSticky'] = enablesessionsticky
        if check_interval is not None:
            kwargs['CheckInterval'] = check_interval
        if check_rise is not None:
            kwargs['CheckRise'] = check_rise
        if check_fall is not None:
            kwargs['CheckFall'] = check_fall
        kwargs['CheckTimeout'] = check_timeout
        if domain is not None:
            kwargs['Domain'] = domain
        if location is not None:
            kwargs['Location'] = location
        if cookie_name is not None:
            kwargs['CookieName'] = cookie_name
        if check_url is not None:
            kwargs['CheckUrl'] = check_url
        if session_mode is not None:
            kwargs['SessionMode'] = session_mode
        if session_timeout is not None:
            kwargs['SessionTimeout'] = session_timeout
        if certificate_id is not None:
            kwargs['CertificateId'] = certificate_id
        return self.request(**kwargs)

    @utils.expect('ListenerSet')
    def DescribeLoadBalancerListeners(self, ids=None, limit=0, offset=0, filters=None):
        """ 获取指定或全部监听转发策略列表

        :param ids: 期望获取的Listener列表
        :type ids: list
        :param limit: 最多返回数量
        :type limit: int
        :param offset: 返回Listener的偏移量，用于分页显示
        :type offset: int
        :param filters: 过滤器，一个dict，包含过滤字段名和值，可能过滤字段为：name, status
        :type filters: dict

        :returns: ListenerSet
        """
        kwargs = {}
        if isinstance(ids, list) and len(ids) > 0:
            kwargs['ListenerId'] = ids
        self.parse_list_params(limit, offset, filters, kwargs)
        return self.request(**kwargs)

    def DeleteLoadBalancerListener(self, listener_id):
        """ 删除ELB Listener

        :param listener_id: ELB listener id
        :type listener_id: string
        :return: 请求是否成功
        """
        kwargs = {'ListenerId': listener_id}
        val = self.request(**kwargs)
        return val

    @utils.expect('Backend')
    def RegisterBackendWithListener(self, listener_id, server_id, name, weight=None, port=None):
        """ 给 Listener 添加后端转发

        :param listener_id: ELB listener id
        :type listener_id: string
        :param server_id: Server id
        :type server_id: string
        :param name: Server customize name
        :type name: string
        :param weight: Forwarding weight
        :type weight: int
        :param port: Forwarding port
        :type port: int

        :return: Backend
        """
        kwargs = {'ListenerId': listener_id, 'ServerId': server_id, 'Name': name}
        if weight is not None:
            kwargs['Weight'] = weight
        if port is not None:
            kwargs['Port'] = port
        return self.request(**kwargs)

    @utils.expect('BackendSet')
    def DescribeListenerBackends(self, listener_id, ids=None, limit=0, offset=0, filters=None):
        """ 获取一个Listener对应的一组或全部后端转发

        :param listener_id: Listener ID
        :type listener_id: string
        :param ids: 期望获取的Listener列表
        :type ids: list
        :param limit: 最多返回数量
        :type limit: int
        :param offset: 返回Backend的偏移量，用于分页显示
        :type offset: int
        :param filters: 过滤器，一个dict，包含过滤字段名和值，可能过滤字段为：name, status
        :type filters: dict

        :returns: BackendSet
        """
        kwargs = {'ListenerId': listener_id}
        if isinstance(ids, list) and len(ids) > 0:
            kwargs['BackendId'] = ids
        self.parse_list_params(limit, offset, filters, kwargs)
        return self.request(**kwargs)

    @utils.expect('Backend')
    def ConfigListenerBackend(self, backend_id, listener_id=None, weight=None, port=None):
        """ 配置Listener Backend

        :param backend_id: Backend id
        :type backend_id: string
        :param listener_id: ELB listener id
        :type listener_id: string
        :param weight: Forwarding weight
        :type weight: int
        :param port: Forwarding port
        :type port: int

        :return: Backend
        """
        kwargs = {'BackendId': backend_id}
        if listener_id is not None:
            kwargs['ListenerId'] = listener_id
        if weight is not None:
            kwargs['Weight'] = weight
        if port is not None:
            kwargs['Port'] = port
        return self.request(**kwargs)

    def DeregisterBackendWithListener(self, id):
        """ 删除指定的后端

        :param id: listener backend id
        :type id: string
        :return: 请求是否成功
        """
        kwargs = {'BackendId': id}
        val = self.request(**kwargs)
        return val
    
    """
        DeepLearning API
    """
    def DescribeDLProjects(self, ids=None, names=None, filters=None,
                          limit=10, offset=0, order_by='id', order='asc'):
        u"""获取深度学习项目列表信息.

        :param ids: 期望获取的DLProjectID列表
        :type ids: list
        :param names: 期望获取信息的DLProject名称列表
        :type names: list
        :param limit: 最多返回数量
        :type limit: int
        :param offset: 返回DLProject的偏移量，用于分页显示
        :type offset: int
        :param filters: 过滤器，一个dict，包含过滤字段名和值，可能过滤字段为：name, status
        :type filters: dict
        :param order_by: 排序字段
        :type order_by: string
        :param order: 值只能为'desc'(升序)或者'asc'(降序)
        :type order: string

        :returns: DLProjectSet，包含DLProject列表
        """
        kwargs = {}
        if isinstance(ids, list) and len(ids) > 0:
            kwargs['DLProjectIds'] = ids
        if isinstance(names, list) and len(names) > 0:
            kwargs['DLProjectNames'] = names
        if order_by and order:
            kwargs['OrderBy'] = order_by
            kwargs['Order'] = order
        self.parse_list_params(limit, offset, filters, kwargs)
        val = self.request(**kwargs)
        return val['DLProjectSet']

    def CreateDLProject(self,
                       name, description=None):
        u"""创建DLProject.

        :param name: 集群名称
        :type name: string
        :param description:
        :type description: string
        :return: DLProject结构
        """
        kwargs = {}
        kwargs['DLProjectName'] = name
        if description:
            kwargs['Description'] = description
        val = self.request(**kwargs)
        return val['DLProject']
    
    def DeleteDLProject(self, idstr):
        u"""删除DLProject.

        :param idstr: DLProjectID
        :type idstr: string
        :return:
        """
        kwargs = {}
        kwargs['DLProjectId'] = idstr
        self.request(**kwargs)

    def UpdateDLProject(self, idstr, name, desc=None):
        u"""更新DLProject.

        :param idstr: DLProjectID
        :type idstr: string
        :return:
        """
        kwargs = {}
        kwargs['DLProjectId'] = idstr
        kwargs['DLProjectName'] = name
        if desc and not desc.isspace():
            kwargs['Description'] = desc
        val = self.request(**kwargs)  # 利用sys._getframe(level).f_code.co_name获取动态运行时的函数名, 在ec2/action目录下
        return val
    
    def CreateDLJob(self, project_id, name, hardware_mode, 
                          is_distributed, job_type, code_source,
                          is_tensorboard, is_auto_start,
                          node_num=None, gpu_num=None, code_main_file=None,
                          data_dir=None, ckpt_dir=None, output_dir=None,
                          cmdline_args=None, tensorboard_log_dir=None,
                          notice_uid=None, distribute_files=None,
                          description=None, image_id=None):
        u"""创建DLJob.

        :param name: Job名称
        :type name: string
        :param description:
        :type description: string
        :return: DLJob结构
        """
        kwargs = {}
        kwargs['DLProjectId'] = project_id
        kwargs['DLJobName'] = name
        kwargs['HardwareMode'] = hardware_mode
        kwargs['IsDistributed'] = is_distributed
        kwargs['JobType'] = job_type
        kwargs['CodeSource'] = code_source
        kwargs['IsTensorboard'] = is_tensorboard
        kwargs['IsAutoStart'] = is_auto_start
        
        if node_num:
            kwargs['NodeNum'] = node_num
        if gpu_num:
            kwargs['GpuNum'] = gpu_num
        if code_main_file:
            kwargs['CodeMainFile'] = code_main_file
        if data_dir:
            kwargs['DataDir'] = data_dir
        if ckpt_dir:
            kwargs['CkptDir'] = ckpt_dir
        if output_dir:
            kwargs['OutputDir'] = output_dir
        if isinstance(cmdline_args, list) and len(cmdline_args) > 0:
            kwargs['CmdlineArgs'] = cmdline_args
        if tensorboard_log_dir:
            kwargs['TensorboardLogDir'] = tensorboard_log_dir
        if notice_uid:
            kwargs['NoticeUId'] = notice_uid
        if isinstance(distribute_files, list) and len(distribute_files) > 0:
            kwargs['DistributeFiles'] = distribute_files
        if description:
            kwargs['Description'] = description
        if image_id:
            kwargs['ImageId'] = image_id
        val = self.request(**kwargs)
        if 'DLJob' in val:
            return val['DLJob']
        else:
            return val
    
    def DescribeDLJobs(self, project_id, ids=None, names=None, filters=None,
                          limit=10, offset=0, order_by='id', order='asc'):
        u"""获取某个项目里深度学习任务列表信息.

        :param ids: 期望获取的DLJobID列表
        :type ids: list
        :param names: 期望获取信息的DLJob名称列表
        :type names: list
        :param limit: 最多返回数量
        :type limit: int
        :param offset: 返回DLJob的偏移量，用于分页显示
        :type offset: int
        :param filters: 过滤器，一个dict，包含过滤字段名和值，可能过滤字段为：name, status
        :type filters: dict
        :param order_by: 排序字段
        :type order_by: string
        :param order: 值只能为'desc'(升序)或者'asc'(降序)
        :type order: string

        :returns: DLJobSet，包含DLJob列表
        """
        kwargs = {}
        kwargs['DLProjectId'] = project_id
        if isinstance(ids, list) and len(ids) > 0:
            kwargs['DLJobIds'] = ids
        if isinstance(names, list) and len(names) > 0:
            kwargs['DLJobNames'] = names
        if order_by and order:
            kwargs['OrderBy'] = order_by
            kwargs['Order'] = order
        self.parse_list_params(limit, offset, filters, kwargs)
        val = self.request(**kwargs)
        return val['DLJobSet']
    
    def DeleteDLJob(self, idstr):
        u"""删除DLJob.

        :param idstr: DLJobID
        :type idstr: string
        :return:
        """
        kwargs = {}
        kwargs['DLJobId'] = idstr
        self.request(**kwargs)
    
    def UpdateDLJob(self, id, name=None, hardware_mode=None, 
                          is_distributed=None, job_type=None, code_source=None,
                          is_tensorboard=None, is_auto_start=None,
                          node_num=None, gpu_num=None, code_main_file=None,
                          data_dir=None, ckpt_dir=None, output_dir=None,
                          cmdline_args=None, tensorboard_log_dir=None,
                          notice_uid=None, distribute_files=None,
                          description=None, image_id=None):
        u"""更新DLJob.

        :param name: Job名称
        :type name: string
        :param description:
        :type description: string
        :return: DLJob结构
        """
        kwargs = {}
        kwargs['DLJobId'] = id
        if name:
            kwargs['DLJobName'] = name
        if hardware_mode:
            kwargs['HardwareMode'] = hardware_mode
        if is_distributed:
            kwargs['IsDistributed'] = is_distributed
        if job_type:
            kwargs['JobType'] = job_type
        if code_source:
            kwargs['CodeSource'] = code_source
        if is_tensorboard:
            kwargs['IsTensorboard'] = is_tensorboard
        if is_auto_start:
            kwargs['IsAutoStart'] = is_auto_start
        
        if node_num:
            kwargs['NodeNum'] = node_num
        if gpu_num:
            kwargs['GpuNum'] = gpu_num
        if code_main_file:
            kwargs['CodeMainFile'] = code_main_file
        if data_dir:
            kwargs['DataDir'] = data_dir
        if ckpt_dir:
            kwargs['CkptDir'] = ckpt_dir
        if output_dir:
            kwargs['OutputDir'] = output_dir
        if isinstance(cmdline_args, list) and len(cmdline_args) > 0:
            kwargs['CmdlineArgs'] = cmdline_args
        if tensorboard_log_dir:
            kwargs['TensorboardLogDir'] = tensorboard_log_dir
        if notice_uid:
            kwargs['NoticeUId'] = notice_uid
        if isinstance(distribute_files, list) and len(distribute_files) > 0:
            kwargs['DistributeFiles'] = distribute_files
        if description:
            kwargs['Description'] = description
        if image_id:
            kwargs['ImageId'] = image_id
        val = self.request(**kwargs)
        if 'DLJob' in val:
            return val['DLJob']
        else:
            return val
    
    def SubmitDLJob(self, idstr):
        u"""提交任务.

        :param idstr: 任务ID
        :type idstr: string
        :return:
        """
        kwargs = {}
        kwargs['DLJobId'] = idstr
        self.request(**kwargs)

    def StopDLJob(self, idstr):
        u"""线束任务.

        :param idstr: 任务ID
        :type idstr: string
        :return:
        """
        kwargs = {}
        kwargs['DLJobId'] = idstr
        self.request(**kwargs)
    
    def DescribeDLImages(self, ids=None, names=None, filters=None,
                          limit=10, offset=0, order_by='id', order='asc'):
        u"""获取深度学习Docker镜像列表信息.

        :param ids: 期望获取的DLImageID列表
        :type ids: list
        :param names: 期望获取信息的DLImage名称列表
        :type names: list
        :param limit: 最多返回数量
        :type limit: int
        :param offset: 返回DLImage的偏移量，用于分页显示
        :type offset: int
        :param filters: 过滤器，一个dict，包含过滤字段名和值，可能过滤字段为：name, status
        :type filters: dict
        :param order_by: 排序字段
        :type order_by: string
        :param order: 值只能为'desc'(升序)或者'asc'(降序)
        :type order: string

        :returns: DLImageSet，包含DLImage列表
        """
        kwargs = {}
        if isinstance(ids, list) and len(ids) > 0:
            kwargs['DLImageIds'] = ids
        if isinstance(names, list) and len(names) > 0:
            kwargs['DLImageNames'] = names
        if order_by and order:
            kwargs['OrderBy'] = order_by
            kwargs['Order'] = order
        self.parse_list_params(limit, offset, filters, kwargs)
        val = self.request(**kwargs)
        return val['DLImageSet']

    def CreateDLImage(self,
                       name, image_config, description=None):
        u"""创建DLImage.
        """
        kwargs = {}
        kwargs['DLImageName'] = name
        kwargs['ImageConfig'] = image_config
        if description:
            kwargs['Description'] = description
        val = self.request(**kwargs)
        return val['DLImage']
    
    def DeleteDLImage(self, idstr):
        u"""删除DLImage.

        :param idstr: DLImageID
        :type idstr: string
        :return:
        """
        kwargs = {}
        kwargs['DLImageId'] = idstr
        self.request(**kwargs)

    def UpdateDLImage(self, idstr, name=None, image_config=None, desc=None):
        u"""更新DLImage.
        """
        kwargs = {}
        kwargs['DLImageId'] = idstr
        if name:
            kwargs['DLImageName'] = name
        if image_config:
            kwargs['ImageConfig'] = image_config
        if desc and not desc.isspace():
            kwargs['Description'] = desc
        val = self.request(**kwargs)  # 利用sys._getframe(level).f_code.co_name获取动态运行时的函数名, 在ec2/action目录下
        return val
