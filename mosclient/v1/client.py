import re

from mosclient.common import utils
from mosclient.common.client import BaseClient


def match_duration(string):
    if re.match(r'^\d+[HhMm]$', string):
        return True
    return False


class Client(BaseClient):

    def DescribeInstanceTypes(self, limit=0, offset=0, filters=None):
        """
        List all instance types
        limit: integer, maximal count of returned items
        offset: integer, offset of return items
        filters: dict, filter conditions
                 filter keys: name, status
        """
        kwargs = {}
        self.parse_list_params(limit, offset, filters, kwargs)
        val = self.request(**kwargs)
        return val['InstanceTypeSet']

    def DescribeTemplates(self):
        """
        List all image templates
        """
        val = self.request()
        return val['TemplateSet']

    def GetBalance(self):
        """
        Get Account Balance
        """
        val = self.request()
        return val

    def DescribeInstances(self, ids=None, names=None, limit=0, offset=0,
                                filters=None):
        """
        List instances
        ids: list, ids of expected instances
        names: list, names of expected instances
        limit: integer, maximal return items
        offset: integer, offset of return items
        filters: dict, filter conditions
                filter key: status, name
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
        """
        List all volumes of an instance
        iid: string, ID of instance
        limit: integer, maximal returned items
        offset: integer, offset of returned items
        filters: dict, filter conditions
        """
        kwargs = {}
        kwargs['InstanceId'] = iid
        self.parse_list_params(limit, offset, filters, kwargs)
        val = self.request(**kwargs)
        return val['InstanceVolumeSet']

    def DescribeInstanceNetworkInterfaces(self, iid, limit=0, offset=0,
                                                filters=None):
        """
        List all network interfaces of an instance
        iid: string, ID of instance
        limit: integer, maximal returned items
        offset: integer, offset of returned items
        filters: dict, filter conditions
        """
        kwargs = {}
        kwargs['InstanceId'] = iid
        self.parse_list_params(limit, offset, filters, kwargs)
        val = self.request(**kwargs)
        return val['InstanceNetworkInterfaceSet']

    def RenewInstance(self, iid, duration=None):
        """
        Renew instance
        iid: string, ID of instance
        duration: string, renew duration, default is 1M
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
        """
        Get contract information of an instance
        iid: string, id of instance
        """
        kwargs = {}
        kwargs['InstanceId'] = iid
        return self.request(**kwargs)

    def CreateInstance(self, imageid, itype, duration=None, name=None,
            keypair=None):
        """
        Create an instance
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
        val = self.request(**kwargs)
        return val['Instance']

    def DescribeInstanceStatus(self, iid):
        """
        Get status of an instance
        """
        kwargs = {}
        kwargs['InstanceId'] = iid
        val = self.request(**kwargs)
        return val['InstanceStatus']

    def GetPasswordData(self, iid, key_file=None):
        """
        Get password data of an instance
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
        """
        Start an instance
        """
        kwargs = {}
        kwargs['InstanceId'] = iid
        self.request(**kwargs)

    def StopInstance(self, iid, force=False):
        """
        Stop an instance
        """
        kwargs = {}
        kwargs['InstanceId'] = iid
        if force:
            kwargs['Force'] = force
        self.request(**kwargs)

    def RebootInstance(self, iid):
        """
        Reboot an instance
        """
        kwargs = {}
        kwargs['InstanceId'] = iid
        self.request(**kwargs)

    def TerminateInstance(self, iid):
        """
        Terminate an instance
        """
        kwargs = {}
        kwargs['InstanceId'] = iid
        self.request(**kwargs)

    def RebuildInstanceRootImage(self, iid, image_id=None):
        """
        Rebuild root image of an instance
        """
        kwargs = {}
        kwargs['InstanceId'] = iid
        if image_id is not None and len(image_id) > 0:
            kwargs['ImageId'] = image_id
        self.request(**kwargs)

    def ChangeInstanceType(self, iid, itype, duration=None):
        """
        Change instance type
        """
        kwargs = {}
        kwargs['InstanceId'] = iid
        kwargs['InstanceType'] = itype
        if duration is not None:
            if match_duration(duration):
                kwargs['Duration'] = duration
            else:
                raise Exception('IIlegal duration format')
        self.request(**kwargs)

    def GetInstanceMetadata(self, iid):
        """
        Get metadata of an instance
        """
        kwargs = {}
        kwargs['InstanceId'] = iid
        val = self.request(**kwargs)
        return val['InstanceMetadata']

    def PutInstanceMetadata(self, iid, data):
        """
        Save metadata of an instance
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
        """
        List all keypairs
        """
        kwargs = {}
        self.parse_list_params(limit, offset, filters, kwargs)
        val = self.request(**kwargs)
        return val['KeyPairSet']

    def ImportKeyPair(self, name, pubkey):
        """
        Import SSH keypair
        """
        kwargs = {}
        kwargs['KeyName'] = name
        kwargs['PublicKeyMaterial'] = pubkey
        val = self.request(**kwargs)
        return val['KeyPair']

    def DeleteKeyPair(self, kid):
        """
        Delete SSH keypair
        """
        kwargs = {}
        kwargs['KeyName'] = kid
        self.request(**kwargs)
