# -*- encoding: utf-8 -*-

import sys

from mosclient.common import utils


@utils.arg('--limit', metavar='<LIMIT>', type=int, help='Limit')
@utils.arg('--offset', metavar='<OFFSET>', type=int, help='Limit')
@utils.arg('--filter', metavar='<FILTER>', action='append', help='Filter')
def do_DescribeInstanceTypes(client, args):
    """ List all instance types """
    val = client.DescribeInstanceTypes(args.limit, args.offset, utils.convert_filter(args.filter))
    utils.print_list(val, 'InstanceType')


def do_DescribeTemplates(client, args):
    """ List all image templates """
    val = client.DescribeTemplates()
    utils.print_list(val, 'Template')


def do_GetBalance(client, args):
    """ Get balance """
    val = client.GetBalance()
    utils.print_dict(val)


@utils.arg('id', metavar='<ID>', help='ID of instance')
@utils.arg('--duration', metavar='<DURATION>', help='Renew instance duration, in H or M, eg 72H, 1M')
def do_RenewInstance(client, args):
    """ Renew an instance """
    client.RenewInstance(args.id, duration=args.duration)


@utils.arg('id', metavar='<ID>', help='ID of instance')
def do_GetInstanceContractInfo(client, args):
    """ Query instance contract information """
    val = client.GetInstanceContractInfo(args.id)
    utils.print_dict(val)


@utils.arg('image', metavar='<IMAGE>', help='ID of image')
@utils.arg('instance_type', metavar='<INSTANCE_TYPE>', help='Instance type')
@utils.arg('--duration', metavar='<DURATION>', help='Reserved instance duration, in H or M, e.g. 72H, 1M')
@utils.arg('--name', metavar='<NAME>', help='Optional instance name')
@utils.arg('--keypair', metavar='<KEYPAIR>', help='SSH key pair name')
@utils.arg('--secgroup', metavar='<SECGROUP>', help='Security group ID')
@utils.arg('--datadisk', metavar='<DISKSIZE>', type=int, help='Extra disksize in GB')
@utils.arg('--bandwidth', metavar='<BANDWIDTH>', type=int, help='Extra external bandwidth in Mbps')
@utils.arg('--zone', metavar='<AVAILABILITYZONE>', type=str, help='Availability Zone')
@utils.arg('--net', metavar='<NETWORK>', type=str, action='append', help="M|Virtual networks\n"
        "Examples:\n"
        "[random]                         random network\n"
        "[random_exit]                    random exit network\n"
        "vnet1:192.168.0.122:10:virtio    network:ipaddress:bwlimit:driver(virtio or e1000)\n")
def do_CreateInstance(client, args):
    """ Create servers """
    val = client.CreateInstance(args.image, args.instance_type,
                                duration=args.duration,
                                name=args.name,
                                keypair=args.keypair,
                                secgroup=args.secgroup,
                                datadisk=args.datadisk,
                                bandwidth=args.bandwidth,
                                zone=args.zone,
                                nets=args.net)
    utils.print_dict(val)


@utils.arg('id', metavar='<ID>', help='ID of instance')
def do_DescribeInstanceStatus(client, args):
    """ Get status of an instance """
    val = client.DescribeInstanceStatus(args.id)
    utils.print_dict(val)


@utils.arg('id', metavar='<ID>', help='ID of instance')
@utils.arg('--key-file', metavar='<PRIVATE_KEY>', help='Private key to decrypt password')
def do_GetPasswordData(client, args):
    """ Get initial password of an instance """
    val = client.GetPasswordData(args.id, key_file=args.key_file)
    utils.print_dict(val)


@utils.arg('--id', metavar='<ID>', action='append', help='ID of instance')
@utils.arg('--name', metavar='<NAME>', action='append', help='Name of instance')
@utils.arg('--group', metavar='<Group>', help='Name or ID of Group')
@utils.arg('--zone', metavar='<AVAILABILITYZONE>', type=str, help='Availability Zone')
@utils.arg('--limit', metavar='<LIMIT>', type=int, help='Limit')
@utils.arg('--offset', metavar='<OFFSET>', type=int, help='Limit')
@utils.arg('--filter', metavar='<FILTER>', action='append', help='Filter')
def do_DescribeInstances(client, args):
    """ Get details of all or specified instances """
    val = client.DescribeInstances(args.id, args.name, args.limit, args.offset, utils.convert_filter(args.filter), args.group, args.zone)
    utils.print_list(val, 'Instance')


@utils.arg('--id', metavar='<ID>', action='append', help='ID of instance')
@utils.arg('--name', metavar='<NAME>', action='append', help='Name of instance')
def do_SearchAssociatedAddresses(client, args):
    """ Get details of all or specified instances """
    val = client.SearchAssociatedAddresses(args.id, args.name)
    utils.print_list(val, 'InstanceEipInfo')



@utils.arg('id', metavar='<ID>', help='ID of instance')
@utils.arg('--limit', metavar='<LIMIT>', type=int, help='Limit')
@utils.arg('--offset', metavar='<OFFSET>', type=int, help='Limit')
@utils.arg('--filter', metavar='<FILTER>', action='append', help='Filter')
def do_DescribeInstanceVolumes(client, args):
    """ List all disks of an instance """
    val = client.DescribeInstanceVolumes(args.id, args.limit, args.offset, utils.convert_filter(args.filter))
    utils.print_list(val, 'InstanceVolume')


@utils.arg('id', metavar='<ID>', help='ID of instance')
@utils.arg('--limit', metavar='<LIMIT>', type=int, help='Limit')
@utils.arg('--offset', metavar='<OFFSET>', type=int, help='Limit')
@utils.arg('--filter', metavar='<FILTER>', action='append', help='Filter')
def do_DescribeInstanceNetworkInterfaces(client, args):
    """ List all network interfaces of an instance """
    val = client.DescribeInstanceNetworkInterfaces(args.id, args.limit, args.offset, utils.convert_filter(args.filter))
    utils.print_list(val, 'InstanceNetworkInterface')


@utils.arg('id', metavar='<ID>', help='ID of instance')
def do_StartInstance(client, args):
    """ Start an instance """
    client.StartInstance(args.id)


@utils.arg('id', metavar='<ID>', help='ID of instance')
@utils.arg('--force', action='store_true', help='Force stop running instance')
def do_StopInstance(client, args):
    """ Stop an instance """
    client.StopInstance(args.id, force=args.force)


@utils.arg('id', metavar='<ID>', help='ID of instance')
def do_RebootInstance(client, args):
    """ Reboot an instance """
    client.RebootInstance(args.id)


@utils.arg('id', metavar='<ID>', help='ID of instance')
def do_TerminateInstance(client, args):
    """ Terminate an instance """
    client.TerminateInstance(args.id)


@utils.arg('id', metavar='<ID>', help='ID of instance')
@utils.arg('--image', metavar='<IMAGE>', help='ID of root image template')
def do_RebuildInstanceRootImage(client, args):
    """ Rebuild root image of an instance """
    client.RebuildInstanceRootImage(args.id, image_id=args.image)


@utils.arg('id', metavar='<ID>', help='ID of instance')
@utils.arg('instance_type', metavar='<INSTANCE_TYPE>', help='Instance type')
@utils.arg('--duration', metavar='<DURATION>', help='Reserved instance duration, in H or M, e.g. 72H, 1M')
@utils.arg('--datadisk', metavar='<DISKSIZE>', required=True, type=int, help='Extra disksize in GB')
@utils.arg('--bandwidth', metavar='<BANDWIDTH>', required=True, type=int, help='Extra external bandwidth in Mbps')
def do_ChangeInstanceType(client, args):
    """ Change instance type """
    client.ChangeInstanceType(args.id, args.instance_type, duration=args.duration,
                              datadisk=args.datadisk, bandwidth=args.bandwidth)


@utils.arg('id', metavar='<ID>', help='ID of instance')
def do_GetInstanceMetadata(client, args):
    """ Get metadata of an instance """
    val = client.GetInstanceMetadata(args.id)
    utils.print_dict(val)


@utils.arg('id', metavar='<ID>', help='ID of instance')
@utils.arg('--data', metavar='<KEY:VALUE>', action='append', help='Key and value pair, separated by coma:')
def do_PutInstanceMetadata(client, args):
    """ Put metadata of an instance """
    data = {}
    if args.data:
        for d in args.data:
            if d.find(':') > 0:
                k = d[:d.find(':')]
                v = d[(d.find(':')+1):]
            else:
                k = d
                v = ''
            data[k] = v
    if len(data) == 0:
        raise Exception('No data to put')
    client.PutInstanceMetadata(args.id, data)


@utils.arg('--limit', metavar='<LIMIT>', type=int, help='Limit')
@utils.arg('--offset', metavar='<OFFSET>', type=int, help='Limit')
@utils.arg('--filter', metavar='<FILTER>', action='append', help='Filter')
def do_DescribeKeyPairs(client, args):
    """ List all keypairs """
    val = client.DescribeKeyPairs(args.limit, args.offset, utils.convert_filter(args.filter))
    utils.print_list(val, 'KeyPair')


@utils.arg('name', metavar='<NAME>', type=str, help='Name of keypair')
@utils.arg('--key-file', metavar='<PUBLIC_KEY_FILE>', type=str, help='Public key file path')
def do_ImportKeyPair(client, args):
    """ Import SSH keypairs """
    if args.key_file is not None:
        with open(args.key_file) as pf:
            pubkey = pf.read()
    else:
        pubkey = sys.stdin.read()
    if pubkey is not None and len(pubkey) > 0:
        val = client.ImportKeyPair(args.name, pubkey)
        utils.print_dict(val)
    else:
        raise Exception('No public key provided')


@utils.arg('id', metavar='<ID>', type=str, help='ID of keypair')
def do_DeleteKeyPair(client, args):
    """ Delete a keypair """
    client.DeleteKeyPair(args.id)


@utils.arg('--iid', metavar='<INSTANCE_ID>', help='ID of instance')
def do_DescribeInstanceMetrics(client, args):
    """List monitor metrics"""
    val = client.DescribeInstanceMetrics(args.iid)
    utils.print_list(val, 'Metric')


@utils.arg('--limit', metavar='<LIMIT>', type=int, help='Limit')
@utils.arg('--offset', metavar='<OFFSET>', type=int, help='Limit')
def do_DescribeAlarmHistory(client, args):
    """List monitor alarm history"""
    val = client.DescribeAlarmHistory(args.limit, args.offset)
    utils.print_list(val, 'AlarmHistory')


@utils.arg('--iid', metavar='<INSTANCE_ID>', required=True, help='Instance ID')
@utils.arg('--metric', metavar='<METRIC>', required=True, help='Metric Name')
@utils.arg('--threshold', metavar='<THRESHOLD>', required=True, help='Threshold')
@utils.arg('--operator', metavar='<OPERATOR>', choices=['GT', 'EQ', 'LT'], required=True, help='Operator')
@utils.arg('--description', metavar='<DESCRIPTION>', help='Monitor description')
def do_CreateMetricAlarm(client, args):
    """Create metric check monitor"""
    val = client.CreateMetricAlarm(args.iid, args.metric, args.operator, args.threshold, args.description)
    utils.print_dict(val)


def do_DescribeMetricAlarms(client, args):
    """List metric check"""
    val = client.DescribeMetricAlarms()
    utils.print_list(val, 'MetricAlarm')


@utils.arg('mid', metavar='<MONITOR_ID>', help='ID of monitor')
def do_DeleteMetricAlarm(client, args):
    """Delete metric check"""
    val = client.DeleteMetricAlarm(args.mid)
    utils.print_dict(val)


@utils.arg('mid', metavar='<MONITOR_ID>', help='ID of monitor')
def do_EnableMetricAlarm(client, args):
    """Enable a metric check"""
    val = client.EnableMetricAlarm(args.mid)
    utils.print_dict(val)


@utils.arg('mid', metavar='<MONITOR_ID>', help='ID of monitor')
def do_DisableMetricAlarm(client, args):
    """Disable a metric check"""
    val = client.DisableMetricAlarm(args.mid)
    utils.print_dict(val)


@utils.arg('--iid', metavar='<INSTANCE_ID>', required=True, help='Instance ID')
@utils.arg('--description', metavar='<DESCRIPTION>', help='Monitor description')
def do_CreateAliveAlarm(client, args):
    """Create alive check"""
    val = client.CreateAliveAlarm(args.iid, args.description)
    utils.print_dict(val)


def do_DescribeAliveAlarms(client, args):
    """List alive check"""
    val = client.DescribeAliveAlarms()
    utils.print_list(val, 'AliveAlarm')


@utils.arg('mid', metavar='<MONITOR_ID>', help='ID of monitor')
def do_DeleteAliveAlarm(client, args):
    """Delete alive check"""
    val = client.DeleteAliveAlarm(args.mid)
    utils.print_dict(val)


@utils.arg('mid', metavar='<MONITOR_ID>', help='ID of monitor')
def do_EnableAliveAlarm(client, args):
    """Enable a alive check"""
    val = client.EnableAliveAlarm(args.mid)
    utils.print_dict(val)


@utils.arg('mid', metavar='<MONITOR_ID>', help='ID of monitor')
def do_DisableAliveAlarm(client, args):
    """Disable a alive check"""
    val = client.DisableAliveAlarm(args.mid)
    utils.print_dict(val)


@utils.arg('--iid', metavar='<INSTANCE_ID>', required=True, help='Instance ID')
@utils.arg('--tcp-port', metavar='<PORT>', required=True, help='TCP port')
@utils.arg('--description', metavar='<DESCRIPTION>', help='Monitor description')
def do_CreateTCPAlarm(client, args):
    """Create tcp check"""
    val = client.CreateTCPAlarm(args.iid, args.tcp_port, args.description)
    utils.print_dict(val)


def do_DescribeTCPAlarms(client, args):
    """List tcp check"""
    val = client.DescribeTCPAlarms()
    utils.print_list(val, 'TCPAlarm')


@utils.arg('mid', metavar='<MONITOR_ID>', help='ID of monitor')
def do_DeleteTCPAlarm(client, args):
    """Delete tcp check"""
    val = client.DeleteTCPAlarm(args.mid)
    utils.print_dict(val)


@utils.arg('mid', metavar='<MONITOR_ID>', help='ID of monitor')
def do_EnableTCPAlarm(client, args):
    """Enable a tcp check"""
    val = client.EnableTCPAlarm(args.mid)
    utils.print_dict(val)


@utils.arg('mid', metavar='<MONITOR_ID>', help='ID of monitor')
def do_DisableTCPAlarm(client, args):
    """Disable a tcp check"""
    val = client.DisableTCPAlarm(args.mid)
    utils.print_dict(val)


@utils.arg('id', metavar='<INSTANCE_ID>', help='ID of tempalte')
@utils.arg('name', metavar='<TEMPLATE_NAME>', help='Name of template')
@utils.arg('--notes', metavar='<NOTES>', help='Template Notes')
def do_CreateTemplate(client, args):
    """Save root disk to new image and upload to glance."""
    val = client.CreateTemplate(args.id, args.name, notes=args.notes)
    utils.print_dict(val)

@utils.arg('id', metavar='<TEMPLATE_ID>', help='ID of template')
def do_DeleteTemplate(client, args):
    """ Delete a template """
    client.DeleteTemplate(args.id)

@utils.arg('name', metavar='<GROUP_NAME>', help='Name of security group')
@utils.arg('description', metavar='<DESCRIPTION>', help='Description of security group')
def do_CreateSecurityGroup(client, args):
    """ Create a security group """
    val = client.CreateSecurityGroup(args.name, args.description)
    utils.print_dict(val)


@utils.arg('--id', metavar='<ID>', action='append', help='ID of security group')
@utils.arg('--name', metavar='<NAME>', action='append', help='Name of security group')
@utils.arg('--limit', metavar='<NUMBER>', default=20, help='Page limit')
@utils.arg('--offset', metavar='<OFFSET>', help='Page offset')
@utils.arg('--filter', metavar='<FILTER>', action='append', help='Filter')
def do_DescribeSecurityGroups(client, args):
    """ List all security groups """
    #p = utils.convert_filter(args.filter)
    val = client.DescribeSecurityGroups(args.id, args.name, args.limit, args.offset, utils.convert_filter(args.filter))
    utils.print_list(val, 'SecurityGroup')


@utils.arg('id', metavar='<GROUP_ID>', help='ID of security group')
def do_DeleteSecurityGroup(client, args):
    """ Delete a security group """
    client.DeleteSecurityGroup(args.id)


@utils.arg('id', metavar='<ID>', help='ID of security group')
@utils.arg('--rule', metavar='<RULE>', action='append', help='Security rule to authorize')
def do_AuthorizeSecurityGroupIngress(client, args):
    """ Authorize an ingress rule to a security group """
    client.AuthorizeSecurityGroupIngress(args.id, args.rule)


@utils.arg('id', metavar='<ID>', help='ID of security group')
@utils.arg('--rule', metavar='<RULE>', action='append', help='Security rule to revoke')
def do_RevokeSecurityGroupIngress(client, args):
    """ Revoke an ingress rule from a security group """
    client.RevokeSecurityGroupIngress(args.id, args.rule)


@utils.arg('iid', metavar='<INSTANCE_ID>', help='ID of instance')
@utils.arg('gid', metavar='<GROUP_ID>', help='ID of security group')
def do_InstanceAssignSecurityGroup(client, args):
    """ Assign a security group to an instance """
    client.InstanceAssignSecurityGroup(args.iid, args.gid)


@utils.arg('iid', metavar='<INSTANCE_ID>', help='ID of instance')
def do_InstanceRevokeSecurityGroup(client, args):
    """ Revoke a security group from an instance """
    client.InstanceRevokeSecurityGroup(args.iid)


@utils.arg('--limit', metavar='<LIMIT>', type=int, help='Limit')
@utils.arg('--offset', metavar='<OFFSET>', type=int, help='Offset')
@utils.arg('--filter', metavar='<FILTER>', action='append', help='Filter')
def do_DescribeAvailabilityZones(client, args):
    """ List all availability zones """
    val = client.DescribeAvailabilityZones(args.limit, args.offset, utils.convert_filter(args.filter))
    utils.print_list(val, 'AvailabilityZone')


@utils.arg('--id', metavar='<ID>', action='append', help='ID of redis')
@utils.arg('--name', metavar='<NAME>', action='append', help='Name of redis')
@utils.arg('--limit', metavar='<LIMIT>', type=int, help='Limit')
@utils.arg('--offset', metavar='<OFFSET>', type=int, help='Limit')
@utils.arg('--filter', metavar='<FILTER>', action='append', help='Filter')
def do_DescribeRedis(client, args):
    """ Get details of all or specified redis """
    val = client.DescribeRedis(args.id, args.name, args.limit, args.offset, utils.convert_filter(args.filter))
    utils.print_list(val, 'Redis')


@utils.arg('--mem', metavar='<MEMORY>', required=True, type=int, help='Redis memory size(GB)')
@utils.arg('--duration', metavar='<DURATION>', help='Reserved redis duration, in H or M, e.g. 72H, 1M')
@utils.arg('--name', metavar='<NAME>', help='Optional redis name')
@utils.arg('--zone', metavar='<ZONE>', help='Zone')
def do_CreateRedis(client, args):
    """ Create redis """
    val = client.CreateRedis(args.mem,
                            duration=args.duration,
                            name=args.name,
                            zone=args.zone)

    utils.print_dict(val)


@utils.arg('id', metavar='<ID>', help='ID of redis')
def do_TerminateRedis(client, args):
    """ Terminate a Redis"""
    client.TerminateRedis(args.id)


@utils.arg('id', metavar='<ID>', help='ID of Redis')
@utils.arg('--duration', metavar='<DURATION>', help='Renew redis duration, in H or M, eg 72H, 1M')
def do_RenewRedis(client, args):
    """ Renew a Redis """
    client.RenewRedis(args.id, duration=args.duration)


@utils.arg('id', metavar='<ID>', help='ID of redis')
@utils.arg('memory', metavar='<MEMORY>', help='Redis memory size(GB)')
@utils.arg('--duration', metavar='<DURATION>', help='Reserved redis duration, in H or M, e.g. 72H, 1M')
def do_ChangeRedisType(client, args):
    """ Change Redis type """
    client.ChangeRedisType(args.id, args.memory, duration=args.duration)


@utils.arg('id', metavar='<ID>', help='ID of redis')
def do_GetRedisContractInfo(client, args):
    """ Query redis contract information """
    val = client.GetRedisContractInfo(args.id)
    utils.print_dict(val)


@utils.arg('--rid', metavar='<REDIS_ID>', required=True, help='Redis ID')
@utils.arg('--metric', metavar='<METRIC>', required=True, help='Metric Name')
@utils.arg('--threshold', metavar='<THRESHOLD>', required=True, help='Threshold')
@utils.arg('--operator', metavar='<OPERATOR>', choices=['GT', 'EQ', 'LT'], required=True, help='Operator')
@utils.arg('--description', metavar='<DESCRIPTION>', help='Monitor description')
def do_CreateRedisAlarm(client, args):
    """Create redis metric check monitor"""
    val = client.CreateRedisAlarm(args.rid, args.metric, args.operator, args.threshold, args.description)
    utils.print_dict(val)


def do_DescribeRedisAlarms(client, args):
    """List redis metric check"""
    val = client.DescribeRedisAlarms()
    utils.print_list(val, 'RedisAlarm')


@utils.arg('mid', metavar='<MONITOR_ID>', help='ID of monitor')
def do_DeleteRedisAlarm(client, args):
    """Delete redis metric check"""
    val = client.DeleteRedisAlarm(args.mid)
    utils.print_dict(val)


@utils.arg('mid', metavar='<MONITOR_ID>', help='ID of monitor')
def do_EnableRedisAlarm(client, args):
    """Enable a metric check"""
    val = client.EnableRedisAlarm(args.mid)
    utils.print_dict(val)


@utils.arg('mid', metavar='<MONITOR_ID>', help='ID of monitor')
def do_DisableRedisAlarm(client, args):
    """Disable a metric check"""
    val = client.DisableRedisAlarm(args.mid)
    utils.print_dict(val)


@utils.arg('--rid', metavar='<REDIS_ID>', help='ID of redis')
def do_DescribeRedisMetrics(client, args):
    """List monitor metrics"""
    val = client.DescribeRedisMetrics(args.rid)
    utils.print_list(val, 'Metric')


@utils.arg('rds_type', metavar='<RDS_TYPE>', help='RDS type')
@utils.arg('datadisk', metavar='<DISKSIZE>', type=int, help='Extra disksize in GB')
@utils.arg('name', metavar='<NAME>', help='RDS name')
@utils.arg('--engine', metavar='<ENGINE>', required=True, help='RDS engine')
@utils.arg('--username', metavar='<USERNAME>', required=True, help='RDS username')
@utils.arg('--password', metavar='<PASSWORD>', required=True, help='RDS password')
@utils.arg('--zone', metavar='<ZONE>', help='Availabble zone')
@utils.arg('--duration', metavar='<DURATION>', help='Reserved rds duration, in H or M, e.g. 72H, 1M')
@utils.arg('--slave_count', metavar='<SLAVE_COUNT>', type=int, help='slave count')
@utils.arg('--proxy_count', metavar='<PROXY_COUNT>', type=int, help='proxy count')
def do_CreateRDS(client, args):
    """ Create rds """
    val = client.CreateRDS(args.rds_type,
                        args.datadisk,
                        args.engine,
                        args.username,
                        args.password,
                        args.name,
                        args.zone,
                        args.duration,
                        slave_count=args.slave_count,
                        proxy_count=args.proxy_count,
                        )
    utils.print_dict(val)


@utils.arg('--id', metavar='<ID>', action='append', help='ID of rds')
@utils.arg('--name', metavar='<NAME>', action='append', help='Name of rds')
@utils.arg('--limit', metavar='<LIMIT>', type=int, help='Limit')
@utils.arg('--offset', metavar='<OFFSET>', type=int, help='Offset')
@utils.arg('--filter', metavar='<FILTER>', action='append', help='Filter')
@utils.arg('--zone', metavar='<AvailabilityZoneId>', help='AvailabilityZoneId')
def do_DescribeRDS(client, args):
    """ Get details of all or specified rds """
    val = client.DescribeRDS(args.id, args.name, args.limit, args.offset, utils.convert_filter(args.filter), args.zone)
    utils.print_list(val, 'RDS')


@utils.arg('id', metavar='<ID>', help='ID of rds')
def do_StartRDS(client, args):
    """ Start an rds """
    client.StartRDS(args.id)


@utils.arg('id', metavar='<ID>', help='ID of rds')
@utils.arg('--force', action='store_true', help='Force stop running rds')
def do_StopRDS(client, args):
    """ Stop an rds """
    client.StopRDS(args.id, force=args.force)


@utils.arg('id', metavar='<ID>', help='ID of rds')
def do_RestartRDS(client, args):
    """ Reboot an rds """
    client.RestartRDS(args.id)


@utils.arg('id', metavar='<ID>', help='ID of rds')
def do_TerminateRDS(client, args):
    """ Terminate an rds """
    client.TerminateRDS(args.id)


@utils.arg('id', metavar='<ID>', help='ID of rds')
@utils.arg('--rds-type', metavar='<RDS_TYPE>', required=True, help='rds type')
@utils.arg('--datadisk', metavar='<DISKSIZE>', type=int, help='Extra disksize in GB')
@utils.arg('--duration', metavar='<DURATION>', help='Reserved rds duration, in H or M, e.g. 72H, 1M')
def do_ChangeRDSType(client, args):
    """ Change rds type """
    client.ChangeRDSType(args.id, args.rds_type, args.datadisk, args.duration)


@utils.arg('id', metavar='<ID>', help='ID of RDS')
@utils.arg('--duration', metavar='<DURATION>', help='Renew RDS duration, in H or M, eg 72H, 1M')
def do_RenewRDS(client, args):
    """ Renew a RDS """
    client.RenewRDS(args.id, duration=args.duration)


@utils.arg('--limit', metavar='<LIMIT>', type=int, help='Limit')
@utils.arg('--offset', metavar='<OFFSET>', type=int, help='Offset')
@utils.arg('--filter', metavar='<FILTER>', action='append', help='Filter')
def do_DescribeRDSTypes(client, args):
    """ List all rds types """
    val = client.DescribeRDSTypes(args.limit, args.offset, utils.convert_filter(args.filter))
    utils.print_list(val, 'RDSType')


def do_DescribeRDSEngines(client, args):
    """ List all rds engines """
    val = client.DescribeRDSEngines()
    utils.print_list(val, 'RDSEngine')


@utils.arg('id', metavar='<ID>', help='ID of rds')
def do_GetRDSContractInfo(client, args):
    """ Query rds contract information """
    val = client.GetRDSContractInfo(args.id)
    utils.print_dict(val)


@utils.arg('--rid', metavar='<RDS_ID>', required=True, help='RDS ID')
@utils.arg('--metric', metavar='<METRIC>', required=True, help='Metric Name')
@utils.arg('--threshold', metavar='<THRESHOLD>', required=True, help='Threshold')
@utils.arg('--operator', metavar='<OPERATOR>', choices=['GT', 'EQ', 'LT'], required=True, help='Operator')
@utils.arg('--description', metavar='<DESCRIPTION>', help='Monitor description')
def do_CreateRDSAlarm(client, args):
    """Create rds metric check monitor"""
    val = client.CreateRDSAlarm(args.rid, args.metric, args.operator, args.threshold, args.description)
    utils.print_dict(val)


def do_DescribeRDSAlarms(client, args):
    """List redis metric check"""
    val = client.DescribeRDSAlarms()
    utils.print_list(val, 'RDSAlarm')


@utils.arg('mid', metavar='<MONITOR_ID>', help='ID of monitor')
def do_DeleteRDSAlarm(client, args):
    """Delete redis metric check"""
    val = client.DeleteRDSAlarm(args.mid)
    utils.print_dict(val)


@utils.arg('mid', metavar='<MONITOR_ID>', help='ID of monitor')
def do_EnableRDSAlarm(client, args):
    """Enable a metric check"""
    val = client.EnableRDSAlarm(args.mid)
    utils.print_dict(val)


@utils.arg('mid', metavar='<MONITOR_ID>', help='ID of monitor')
def do_DisableRDSAlarm(client, args):
    """Disable a metric check"""
    val = client.DisableRDSAlarm(args.mid)
    utils.print_dict(val)


@utils.arg('--rid', metavar='<RDS_ID>', help='ID of rds')
def do_DescribeRDSMetrics(client, args):
    """List monitor metrics"""
    val = client.DescribeRDSMetrics(args.rid)
    utils.print_list(val, 'Metric')


"""
VPC CRUD
"""


@utils.arg('name', metavar='<NAME>', help='Name of VPC')
@utils.arg('--cidr', metavar='<CIDR>', required=True, help='Choose from \'10.0.0.0/8\', \'172.16.0.0/12\', \'192.168.0.0/16\'')
@utils.arg('--desc', metavar='<VPC_DESCRIPTION>', help='Description of VPC')
def do_CreateVPC(client, args):
    """Create VPC"""
    val = client.CreateVPC(args.name, args.cidr, args.desc)
    utils.print_dict(val, 'VPC')


@utils.arg('id', metavar='<VPC_ID>', help='ID of VPC')
def do_DeleteVPC(client, args):
    """Delete VPC
    暂未开放, 可提工单进行操作。
    """
    # val = client.DeleteVPC(args.id)
    # utils.print_dict(val)
    print "Delete is forbidden!"


@utils.arg('id', metavar='<VPC_ID>', help='ID of VPC')
@utils.arg('--name', metavar='<NAME>', required=True, help='Name of VPC')
@utils.arg('--desc', metavar='<VPC_DESCRIPTION>', help='Description of VPC')
def do_UpdateVPC(client, args):
    """Update VPC"""
    val = client.UpdateVPC(args.id, args.name, args.desc)
    utils.print_dict(val, 'VPC')


@utils.arg('--id', metavar='<VPC_ID>', action='append', help='ID of VPC')
@utils.arg('--zone', metavar='<AVAILABILITYZONE>', type=str, help='Availability Zone')
@utils.arg('--limit', metavar='<LIMIT>', type=int, help='Limit')
@utils.arg('--offset', metavar='<OFFSET>', type=int, help='Offset')
def do_DescribeVPCs(client, args):
    """Describe VPC list"""
    val = client.DescribeVPCs(args.id, args.limit, args.offset, zone=args.zone)
    utils.print_list(val, 'VPC')


"""
VPC Subnet CRUD
"""


@utils.arg('name', metavar='<NAME>', help='Name of VPC')
@utils.arg('--vpcId', metavar='<VPC_ID>', required=True, help='ID of VPC')
@utils.arg('--zoneId', metavar='<AvailabilityZoneId>', required=True, help='Available Zone')
@utils.arg('--startip', metavar='<START_IP>', required=True, help='Start ip of subnet, should within vpc cidr')
@utils.arg('--endip', metavar='<END_IP>', required=True, help='End ip of subnet, should within vpc cidr')
@utils.arg('--netmask', metavar='<NETMASK>', required=True, help='Netmask of subnet')
@utils.arg('--gateway', metavar='<GATEWAY>', required=True, help='Gateway of subnet')
@utils.arg('--desc', metavar='<DESCRIPTION>', help='Description of Subnet')
def do_CreateVPCSubnet(client, args):
    """Create Subnet in VPC"""
    val = client.CreateVPCSubnet(args.name, args.vpcId, args.zoneId, args.startip, args.endip, args.netmask, args.gateway, args.desc)
    utils.print_dict(val, 'VPC')


@utils.arg('id', metavar='<SUBNET_ID>', help='ID of Subnet')
def do_DeleteVPCSubnet(client, args):
    """Delete Subnet of VPC
    暂未开放, 可提工单进行操作。
    """
    # val = client.DeleteVPCSubnet(args.id)
    # utils.print_dict(val)
    print "Delete is forbidden!"


@utils.arg('--id', metavar='<SUBNET_ID>', required=True, help='ID of Subnet')
@utils.arg('--name', metavar='<NAME>', help='Name of VPC')
@utils.arg('--desc', metavar='<DESCRIPTION>', help='Description of Subnet')
def do_UpdateVPCSubnet(client, args):
    """Update Subnet in VPC"""
    val = client.UpdateVPCSubnet(args.id, args.name, args.desc)
    utils.print_dict(val, 'Subnet')


@utils.arg('--id', metavar='<SUBNET_ID>', action='append', help='ID of Subnet')
@utils.arg('--zone', metavar='<AVAILABILITYZONE>', type=str, help='Availability Zone')
@utils.arg('--limit', metavar='<LIMIT>', type=int, help='Limit')
@utils.arg('--offset', metavar='<OFFSET>', type=int, help='Offset')
def do_DescribeVPCSubnets(client, args):
    """Describe Subnet list"""
    val = client.DescribeVPCSubnets(args.id, args.limit, args.offset, zone=args.zone)
    utils.print_list(val, 'Subnet')


@utils.arg('vid', metavar='<VPC_ID>', help='ID of VPC')
@utils.arg('--limit', metavar='<LIMIT>', type=int, help='Limit')
@utils.arg('--offset', metavar='<OFFSET>', type=int, help='Offset')
def do_ListVPCSubnets(client, args):
    """ List VPC Subnets """
    val = client.ListVPCSubnets(args.vid, args.limit, args.offset)
    utils.print_list(val, 'Subnet')


@utils.arg('--name', metavar='<Name>', required=True, help='name of EIP, e.g. "eipA"')
@utils.arg('--billingModel', metavar='<BillingModel>', default='bandwidth', choices=['flow', 'bandwidth'],
           help='BillingType of EIP, by bandwidth or flow')
@utils.arg('--zoneId', metavar='<AvailabilityZoneId>', type=str, help='Availability Zone')
def do_AllocateAddress(client, args):
    """ Allocate EIP """
    val = client.AllocateAddress(args.name, args.billingModel, args.zoneId)
    utils.print_dict(val, 'Address')


@utils.arg('id', metavar='<AllocationId>', help='ID of EIP')
def do_ReleaseAddress(client, args):
    """Release EIP """
    val = client.ReleaseAddress(args.id)
    utils.print_dict(val)


@utils.arg('id', metavar='<AllocationId>', help='ID of EIP')
@utils.arg('--name', metavar='<Name>', help='name of EIP, e.g. "eipA"')
def do_ConfigAddress(client, args):
    """Config EIP """
    val = client.ConfigAddress(args.id, args.name)
    utils.print_dict(val, 'Address')


@utils.arg('id', metavar='<AllocationId>', help='ID of EIP')
@utils.arg('--bandwidth', metavar='<Bandwidth>', help='EIP bandwidth(Mbps), 0-1000')
def do_ConfigAddressBandwidth(client, args):
    """Config EIP Bandwidth"""
    val = client.ConfigAddressBandwidth(args.id, args.bandwidth)
    utils.print_dict(val, 'Address')


@utils.arg('--id', metavar='<ID>', action='append', help='AllocationId of IP')
@utils.arg('--zone', metavar='<AVAILABILITYZONE>', type=str, help='Availability Zone')
@utils.arg('--limit', metavar='<LIMIT>', type=int, help='Limit')
@utils.arg('--offset', metavar='<OFFSET>', type=int, help='Offset')
def do_DescribeAddresses(client, args):
    """Describe EIP list"""
    val = client.DescribeAddresses(args.id, args.limit, args.offset, zone=args.zone)
    utils.print_list(val, 'Address')


@utils.arg('id', metavar='<AllocationId>', help='ID of EIP')
@utils.arg('--associationType', metavar='<AssociationType>', required=True, choices=['server', 'elb'],
           help='EIP Bind Instance Type')
@utils.arg('--instanceId', metavar='<InstanceId>', required=True, help='EIP Bind Instance Id')
@utils.arg('--bandwidth', metavar='<Bandwidth>', required=True, help='EIP Bind Instance Bandwidth (Mbps), 0-1000')
def do_AssociateAddress(client, args):
    """bind eip to cloud service"""
    val = client.AssociateAddress(args.id, args.associationType, args.instanceId, args.bandwidth)
    utils.print_dict(val, 'Address')


@utils.arg('id', metavar='<AllocationId>', help='ID of EIP')
def do_DisassociateAddress(client, args):
    """unbind eip to cloud service"""
    val = client.DisassociateAddress(args.id)
    utils.print_dict(val)

@utils.arg('id', metavar='<AllocationId>', help='ID of EIP')
@utils.arg('--newId', metavar='<NewAllocationId>', required=True, help='ID of new EIP')
@utils.arg('--sync', metavar='<SYNC>', default=False, help='Replace is sync')
@utils.arg('--timeout', metavar='<TIMEOUT>', default=300, help='Timeout')
def do_ReplaceAddress(client, args):
    """replace old eip with new eip"""
    val = client.ReplaceAddress(args.id, args.newId, args.sync, args.timeout)
    utils.print_dict(val, 'Address')

##
#
#   EBS code
#
@utils.arg('--name', metavar='<NAME>', help='Optional ebs name')
@utils.arg('--disksize', metavar='<DISKSIZE>', help='ebs size G')
@utils.arg('--zone', metavar='<ZONE>', help='Zone')
def do_CreateVolume(client, args):
    """ Create Volume """
    val = client.CreateVolume(args.name,
                            disksize=args.disksize,
                            zone=args.zone)

    utils.print_dict(val)

@utils.arg('--ebs_id', metavar='<VolumeId>', action='append', help='Volume Id')
@utils.arg('--zone', metavar='<AVAILABILITYZONE>', type=str, help='Availability Zone')
@utils.arg('--limit', metavar='<LIMIT>', type=int, help='Limit')
@utils.arg('--offset', metavar='<OFFSET>', type=int, help='Offset')
@utils.arg('--filter', metavar='<FILTER>', action='append', help='Offset')
def do_DescribeVolumes(client, args):
    """Describe specific Volume listener info"""
    val = client.DescribeVolumes(args.ebs_id, args.zone, args.limit, args.offset, utils.convert_filter(args.filter))
    utils.print_list(val, 'Volume')

@utils.arg('--ebs_id', metavar='<VolumeId>', required=True, help='ID of Volume')
@utils.arg('--instance_id', metavar='<InstanceId>', required=True, help='ID of Instance')
def do_AttachVolume(client, args):
    """Attach Volume on Instance"""
    val = client.AttachVolume(args.ebs_id, args.instance_id)
    utils.print_dict(val)

@utils.arg('--ebs_id', metavar='<VolumeId>', required=True, help='ID of Volume')
@utils.arg('--instance_id', metavar='<InstanceId>', required=True, help='ID of Instance')
def do_DetachVolume(client, args):
    """Detach Volume"""
    val = client.DetachVolume(args.ebs_id, args.instance_id)
    utils.print_dict(val)

@utils.arg('--ebs_id', metavar='<VolumeId>', required=True, help='ID of Volume')
def do_DeleteVolume(client, args):
    """Delete Volume"""
    val = client.DeleteVolume(args.ebs_id)
    utils.print_dict(val)

@utils.arg('--ebs_snapshot_ids', metavar='<VolumeSnapshotId>', action='append', help='mebsSnapshot Id')
@utils.arg('--zone', metavar='<AVAILABILITYZONE>', type=str, help='Availability Zone')
@utils.arg('--limit', metavar='<LIMIT>', type=int, help='Limit')
@utils.arg('--offset', metavar='<OFFSET>', type=int, help='Offset')
@utils.arg('--filter', metavar='<FILTER>', action='append', help='Offset')
def do_DescribeVolumeSnapshots(client, args):
    """Describe specific Volume Snapshot listener info"""
    val = client.DescribeVolumeSnapshots(args.ebs_snapshot_ids, args.zone, args.limit, args.offset, utils.convert_filter(args.filter))
    utils.print_list(val, 'VolumeSnapshot')

@utils.arg('--ebs_snapshot_id', metavar='<VolumeSnapshotId>', required=True, help='ID of Volume snapshot')
def do_RecoverVolume(client, args):
    """Recover Volume"""
    val = client.RecoverVolume(args.ebs_snapshot_id)
    utils.print_dict(val)

@utils.arg('--ebs_snapshot_id', metavar='<VolumeSnapshotId>', required=True, help='ID of Volume snapshot')
def do_DeleteVolumeSnapshot(client, args):
    """Delete Volume Snapshot"""
    val = client.DeleteVolumeSnapshot(args.ebs_snapshot_id)
    utils.print_dict(val)

"""
    主机分组
"""
@utils.arg('--servergroup_ids', metavar='<ServerGroupId>', action='append', help='ServerGroup Id')
@utils.arg('--zone', metavar='<AVAILABILITYZONE>', type=str, help='Availability Zone')
@utils.arg('--limit', metavar='<LIMIT>', type=int, help='Limit')
@utils.arg('--offset', metavar='<OFFSET>', type=int, help='Offset')
@utils.arg('--filter', metavar='<FILTER>', action='append', help='Offset')
def do_DescribeServerGroup(client, args):
    """Describe ServerGroup info"""
    val = client.DescribeServerGroup(args.servergroup_ids, args.zone, args.limit, args.offset, utils.convert_filter(args.filter))
    utils.print_list(val, 'ServerGroup')

@utils.arg('name', metavar='<Name>', help='Name')
@utils.arg('--zone', metavar='<AvailabilityZoneId>', help='AvailabilityZoneId')
def do_CreateServerGroup(client, args):
    """Create ServerGroup"""
    val = client.CreateServerGroup(args.name, args.zone)
    utils.print_dict(val, 'ServerGroup')

@utils.arg('group', metavar='<Group>', help='Group name or ID')
def do_ReleaseServerGroup(client, args):
    """Delete Group"""
    val = client.ReleaseServerGroup(args.group)
    utils.print_dict(val)

# @utils.arg('instance_id', metavar='<instanceId>', help='instanceId')
# def do_ServerGroupShow(client, args):
#     """Create ServerGroup"""
#     val = client.ServerGroupShow(args.instance_id)
#     utils.print_dict(val, 'ServerGroup')

@utils.arg('--group', metavar='<Group>', action='append', help='Group name or ID')
@utils.arg('--zone', metavar='<AVAILABILITYZONE>', type=str, help='Availability Zone')
@utils.arg('--limit', metavar='<LIMIT>', type=int, help='Limit')
@utils.arg('--offset', metavar='<OFFSET>', type=int, help='Offset')
@utils.arg('--filter', metavar='<FILTER>', action='append', help='Offset')
def do_DescribeServerByGroup(client, args):
    """Describe group instance info"""
    val = client.DescribeServerByGroup(args.group, args.zone, args.limit, args.offset, utils.convert_filter(args.filter))
    utils.print_list(val, 'GroupGuest')

@utils.arg('instance_id', metavar='<instanceId>', help='instanceId')
@utils.arg('group', metavar='<Group>', help='Group Name or ID')
def do_ServerJoinGroup(client, args):
    """join ServerGroup"""
    val = client.ServerJoinGroup(args.group, args.instance_id)
    utils.print_dict(val, 'GroupGuest')

@utils.arg('instance_id', metavar='<instanceId>', help='instanceId')
@utils.arg('group', metavar='<Group>', help='Group Name or ID')
def do_ServerLeaveGroup(client, args):
    """remove ServerGroup"""
    val = client.ServerLeaveGroup(args.group, args.instance_id)
    utils.print_dict(val)

"""
    ECS API
"""
@utils.arg('--ecs', metavar='<ECS>', action='append', help='ECS name or ID')
@utils.arg('--zone', metavar='<AVAILABILITYZONE>', type=str, help='Availability Zone')
@utils.arg('--limit', metavar='<LIMIT>', type=int, help='Limit')
@utils.arg('--offset', metavar='<OFFSET>', type=int, help='Offset')
@utils.arg('--filter', metavar='<FILTER>', action='append', help='Offset')
def do_DescribeECS(client, args):
    """Describe esc instance info"""
    val = client.DescribeECS(args.ecs, args.zone, args.limit, args.offset, utils.convert_filter(args.filter))
    utils.print_list(val, 'ECS')

@utils.arg('name', metavar='<Name>', help='Name')
@utils.arg('flavor', metavar='<Flavor>', help='ECS Type')
@utils.arg('driver', metavar='<Driver>', help='ECS driver (Memcached)')
@utils.arg('--master_count', metavar='<MASTER_COUNT>', type=int ,help='ECS master count')
@utils.arg('--zone', metavar='<AvailabilityZoneId>', help='AvailabilityZoneId')
def do_CreateECS(client, args):
    """Create ECS"""
    val = client.CreateECS(args.name, args.flavor, args.driver, args.master_count, args.zone)
    utils.print_dict(val, 'ECS')

@utils.arg('ecs_id', metavar='<ECS_ID>', help='ECS ID')
@utils.arg('flavor', metavar='<Flavor>', help='ECS Type')
def do_ChangeECSType(client, args):
    """Change ECS Type"""
    val = client.ChangeECSType(args.ecs_id, args.flavor)
    utils.print_dict(val)

@utils.arg('ecs_id', metavar='<ECS_ID>', help='ECS ID')
def do_DeleteECS(client, args):
    """Delete ECS"""
    val = client.DeleteECS(args.ecs_id)
    utils.print_dict(val)

@utils.arg('ecs', metavar='<ECS>', help='ECS name or ID')
@utils.arg('--limit', metavar='<LIMIT>', type=int, help='Limit')
@utils.arg('--offset', metavar='<OFFSET>', type=int, help='Offset')
@utils.arg('--filter', metavar='<FILTER>', action='append', help='Offset')
def do_DescribeECSNode(client, args):
    """Describe esc node instance info"""
    val = client.DescribeECSNode(args.ecs, args.limit, args.offset, utils.convert_filter(args.filter))
    utils.print_list(val, 'RDSNode')

@utils.arg('ecs_id', metavar='<ECS_ID>', help='ECS ID')
@utils.arg('--count', metavar='<COUNT>', type=int, help='ECS COUNT')
def do_CreateECSNode(client, args):
    """Create ECS node"""
    val = client.CreateECSNode(args.ecs_id, args.count)
    utils.print_dict(val)

@utils.arg('node_id', metavar='<NODE_ID>', help='NODE ID')
def do_DeleteCDSNode(client, args):
    """Delete ECS node"""
    val = client.DeleteCDSNode(args.node_id)
    utils.print_dict(val)

@utils.arg('rds', metavar='<RDS>', help='RDS name or ID')
@utils.arg('--limit', metavar='<LIMIT>', type=int, help='Limit')
@utils.arg('--offset', metavar='<OFFSET>', type=int, help='Offset')
@utils.arg('--filter', metavar='<FILTER>', action='append', help='Offset')
def do_DescribeRDSNode(client, args):
    """Describe RDS node instance info"""
    val = client.DescribeRDSNode(args.rds, args.limit, args.offset, utils.convert_filter(args.filter))
    utils.print_list(val, 'RDSNode')

@utils.arg('rds', metavar='<RDS>', help='RDS ID')
@utils.arg('role', metavar='<ROLE>', help='Node Role, choices=(slave, proxy)')
@utils.arg('--count', metavar='<COUNT>', type=int, help='ECS COUNT')
def do_CreateRDSNode(client, args):
    """Create RDS node"""
    val = client.CreateRDSNode(args.rds, args.role, args.count)
    utils.print_dict(val)


"""
    BigData API
"""
@utils.arg('--id', metavar='<ID>', action='append', help='ID of StreamingSystem')
@utils.arg('--name', metavar='<NAME>', action='append', help='Name of StreamingSystem')
@utils.arg('--zone', metavar='<AVAILABILITYZONE>', type=str, help='ID of Zone')
@utils.arg('--limit', metavar='<LIMIT>', type=int, help='Limit')
@utils.arg('--offset', metavar='<OFFSET>', type=int, help='Offset')
@utils.arg('--filter', metavar='<FILTER>', action='append', help='Filter')
@utils.arg('--order_by', metavar='<ORDER_BY>', type=str, help='ORDER_BY')
@utils.arg('--order', metavar='<ORDER>', type=str,
           help='ORDER:["desc", "asc"]')
def do_DescribeSDSystems(client, args):
    """List all StreamingSystem."""
    val = client.DescribeSDSystems(args.id, args.name, args.zone, utils.convert_filter(args.filter),
                           args.limit, args.offset, args.order_by, args.order)
    utils.print_list(val, 'StreamingSystem')


@utils.arg('--id', metavar='<ID>', action='append', help='ID of BigDataSystem')
@utils.arg('--name', metavar='<NAME>', action='append', help='Name of BigDataSystem')
@utils.arg('--zone', metavar='<AVAILABILITYZONE>', type=str, help='ID of Zone')
@utils.arg('--limit', metavar='<LIMIT>', type=int, help='Limit')
@utils.arg('--offset', metavar='<OFFSET>', type=int, help='Offset')
@utils.arg('--filter', metavar='<FILTER>', action='append', help='Filter')
@utils.arg('--order_by', metavar='<ORDER_BY>', type=str, help='ORDER_BY')
@utils.arg('--order', metavar='<ORDER>', type=str,
           help='ORDER:["desc", "asc"]')
def do_DescribeBDSystems(client, args):
    """List all BigDataSystem."""
    val = client.DescribeBDSystems(args.id, args.name, args.zone, utils.convert_filter(args.filter),
                           args.limit, args.offset, args.order_by, args.order)
    utils.print_list(val, 'BigDataSystem')


@utils.arg('id', metavar='<BDS_ID>', type=str, help='ID of BDSystem')
def do_StartBDSystem(client, args):
    """Start the BDSystem."""
    client.StartBDSystem(args.id)


@utils.arg('id', metavar='<BDS_ID>', type=str, help='ID of BDSystem')
def do_StopBDSystem(client, args):
    """Stop the BDSystem."""
    client.StopBDSystem(args.id)


@utils.arg('id', metavar='<BDS_ID>', type=str, help='ID of BDSystem')
def do_DeleteBDSystem(client, args):
    """Delete the BDSystem."""
    client.DeleteBDSystem(args.id)


@utils.arg('id', metavar='<BDS_ID>', type=str, help='ID of BDsystem')
@utils.arg('delta', metavar='<DELTA>', type=int, help='number of nodes')
def do_ScaleUpBDSystem(client, args):
    """Scale-up the BDSystem."""
    client.ScaleUpBDSystem(args.id, args.delta)


@utils.arg('id', metavar='<BDS_ID>', type=str, help='ID of BDSystem')
@utils.arg('delta', metavar='<DELTA>', type=int, help='number of nodes')
def do_ScaleDownBDSystem(client, args):
    """Scale-down the BDSystem."""
    client.ScaleDownBDSystem(args.id, args.delta)


@utils.arg('id', metavar='<SDS_ID>', type=str, help='ID of SDSystem')
def do_StartSDSystem(client, args):
    """Start the SDSystem."""
    client.StartSDSystem(args.id)


@utils.arg('id', metavar='<SDS_ID>', type=str, help='ID of SDSystem')
def do_StopSDSystem(client, args):
    """Stop the SDSystem."""
    client.StopSDSystem(args.id)


@utils.arg('id', metavar='<SDS_ID>', type=str, help='ID of SDSystem')
def do_DeleteSDSystem(client, args):
    """Delete the SDSystem."""
    client.DeleteSDSystem(args.id)


@utils.arg('id', metavar='<SDS_ID>', type=str, help='ID of SDSystem')
@utils.arg('delta', metavar='<DELTA>', type=int, help='number of nodes')
def do_ScaleUpSDSystem(client, args):
    """Scale-up the SDSystem."""
    client.ScaleUpSDSystem(args.id, args.delta)


@utils.arg('id', metavar='<SDS_ID>', type=str, help='ID of SDSystem')
@utils.arg('delta', metavar='<DELTA>', type=int, help='number of nodes')
def do_ScaleDownSDSystem(client, args):
    """Scale-down the SDSystem."""
    client.ScaleDownSDSystem(args.id, args.delta)


@utils.arg('name', metavar='<BDS_NAME>', type=str, help='NAME of BDSystem')
@utils.arg('architecture', metavar='<BDS_ARCHITECTURE>', type=str,
           help='ARCHITECTURE of BDSystem')
@utils.arg('slave_count', metavar='<BDS_SLAVE_COUNT>', type=int,
           help='SLAVE_COUNT of BDSystem')
@utils.arg('--bds_type', metavar='<BDS_FLAVOR>', required=True, type=str,
           help='ID of FLAVOR for BDS')
@utils.arg('--zone', metavar='<ZONE>', required=True, type=str,
           help='ID or NAME of ZONE')
@utils.arg('--admin_pass', metavar='<PASSWORD>', required=True, type=str,
           help='PASSWORD of ADMINISTRATOR')
@utils.arg('--desc', metavar='<DESCRIPTION>', type=str,
           help='DESCRIPTION')
def do_CreateBDSystem(client, args):
    """Create a BDSystem."""
    val = client.CreateBDSystem(args.name, args.architecture,
                                args.slave_count, args.bds_type,
                                args.zone, args.admin_pass, args.desc)
    utils.print_dict(val)


@utils.arg('name', metavar='<SDS_NAME>', type=str, help='NAME of SDSystem')
@utils.arg('architecture', metavar='<SDS_ARCHITECTURE>', type=str,
           help='ARCHITECTURE of SDSystem')
@utils.arg('slave_count', metavar='<SDS_SLAVE_COUNT>', type=int,
           help='SLAVE_COUNT of SDSystem')
@utils.arg('--bds_type', metavar='<SDS_FLAVOR>', required=True, type=str,
           help='ID of FLAVOR for SDS')
@utils.arg('--zone', metavar='<ZONE>', required=True, type=str,
           help='ID or NAME of ZONE')
@utils.arg('--admin_pass', metavar='<PASSWORD>', required=True, type=str,
           help='PASSWORD of ADMINISTRATOR')
@utils.arg('--desc', metavar='<DESCRIPTION>', type=str,
           help='DESCRIPTION')
def do_CreateSDSystem(client, args):
    """Create a SDSystem."""
    val = client.CreateSDSystem(args.name, args.architecture,
                                args.slave_count, args.bds_type,
                                args.zone, args.admin_pass,
                                args.desc)
    utils.print_dict(val)


@utils.arg('--limit', metavar='<LIMIT>', type=int, help='Limit')
@utils.arg('--offset', metavar='<OFFSET>', type=int, help='Offset')
@utils.arg('--filter', metavar='<FILTER>', action='append', help='Filter')
def do_DescribeBDSTypes(client, args):
    """List all BigDataSystem types."""
    val = client.DescribeBDSTypes(args.limit, args.offset, utils.convert_filter(args.filter))
    utils.print_list(val, 'BDSType')


@utils.arg('--limit', metavar='<LIMIT>', type=int, help='Limit')
@utils.arg('--offset', metavar='<OFFSET>', type=int, help='Offset')
@utils.arg('--filter', metavar='<FILTER>', action='append', help='Filter')
def do_DescribeSDSTypes(client, args):
    """List all StreamingSystem types."""
    val = client.DescribeSDSTypes(args.limit, args.offset, utils.convert_filter(args.filter))
    utils.print_list(val, 'SDSType')


@utils.arg('name', metavar='<ELB_NAME>', type=str, help='Name of ELB')
@utils.arg('--allocation_id', metavar="<EIP_ID>", required=True, type=str, help="ID of EIP")
@utils.arg('--bandwidth', metavar='<BANDWIDTH>', required=True, type=int, help='Extra external bandwidth in Mbps')
@utils.arg('--zone', metavar='<AVAILABILITYZONE>', type=str, help='Availability Zone')
def do_CreateLoadBalancer(client, args):
    """Create a ELB instance"""
    val = client.CreateLoadBalancer(args.name, args.allocation_id, args.bandwidth, zone=args.zone)
    utils.print_dict(val)


@utils.arg('id', metavar='<ID>', type=str, help='ID of ELB')
def do_DeleteLoadBalancer(client, args):
    """ Delete a ELB """
    val = client.DeleteLoadBalancer(args.id)
    utils.print_dict(val)


@utils.arg('--id', metavar='<ID>', action='append', help='ID of LoadBalancer')
@utils.arg('--limit', metavar='<LIMIT>', type=int, help='Limit')
@utils.arg('--offset', metavar='<OFFSET>', type=int, help='Offset')
@utils.arg('--zone', metavar='<AVAILABILITYZONE>', type=str, help='Availability Zone')
def do_DescribeLoadBalancers(client, args):
    """List all ELB instances"""
    val = client.DescribeLoadBalancers(args.id, args.limit, args.offset, args.zone)
    utils.print_list(val, 'LoadBalancer')


@utils.arg('id', metavar='<ELB_ID>', type=str, help='ID of ELB')
@utils.arg('--allocation_id', metavar="<EIP_ID>", type=str, help="ID or IP of EIP")
@utils.arg('--bandwidth', metavar='<BANDWIDTH>', type=int, help='Extra external bandwidth in Mbps')
@utils.arg('--name', metavar='<ELB_NAME>', type=str, help='Name of ELB')
def do_ModifyLoadBalancerAttributes(client, args):
    """Modify a ELB instance"""
    val = client.ModifyLoadBalancerAttributes(args.id, args.name, args.bandwidth, args.allocation_id)
    utils.print_dict(val)


@utils.arg('name', metavar='<LISTENER_NAME>', type=str, help='Name of ELB Listener')
@utils.arg('--alg', metavar='<ALG>', required=True, type=str, help="Forwarding strategy, select in ['wrr', 'rr']")
@utils.arg('--protocol', metavar='<PROTOCOL>', required=True, type=str, help="Forwarding protocol, select in ['TCP', 'HTTP', 'HTTPS']")
@utils.arg('--frontend_port', metavar='<FRONTEND_PORT>', required=True, type=int, help="External serve port")
@utils.arg('--backend_port', metavar='<BACKEND_PORT>', required=True, type=int, help="Backend forwarded port")
@utils.arg('--enablesessionsticky', action='store_true')
@utils.arg('--elb_id', metavar="<ELB_ID>", required=True, type=str, help="ID of LoadBalancer")
@utils.arg('--check_interval', metavar='<CHECK_INTERVAL>', type=int, default=5, help='Health check interval, default 5s')
@utils.arg('--check_rise', metavar='<CHECK_RISE>', type=int, help='Check failed times treat backend available')
@utils.arg('--check_fall', metavar='<CHECK_FALL>', type=int, help='Check failed times treat backend not available')
@utils.arg('--check_timeout', metavar='<CHECK_TIMEOUT>', type=int, default=3, help='Check timeout, default=3s')
@utils.arg('--domain', metavar='<DOMAIN>', type=str, help='Domain name corresponding to forwarding rules')
@utils.arg('--location', metavar='<LOCATION>', type=str, help='URL location corresponding to forwarding rules')
@utils.arg('--cookie_name', metavar='<COOKIENAME>', type=str, help='Cookie name keep in session')
@utils.arg('--check_url', metavar='<CHECK_URL>', type=str, help='Health check url')
@utils.arg('--session_mode', metavar='<SESSION_MODE>', type=str, help='Session keep mode')
@utils.arg('--session_timeout', metavar='<SESSION_TIMEOUT>', type=int, help='Session timeout')
@utils.arg('--certificate_id', metavar='<CERTIFICATEID>', type=str, help='Https certificate id')
def do_CreateLoadBalancerListener(client, args):
    """Create a ELB instance"""
    val = client.CreateLoadBalancerListener(args.name, args.alg, args.protocol,
                                            args.frontend_port, args.backend_port,
                                            args.elb_id, args.enablesessionsticky,
                                            check_interval=args.check_interval,
                                            check_rise=args.check_rise,
                                            check_fall=args.check_fall,
                                            check_timeout=args.check_timeout,
                                            domain=args.domain, location=args.location,
                                            cookie_name=args.cookie_name,
                                            check_url=args.check_url,
                                            session_mode=args.session_mode,
                                            session_timeout=args.session_timeout,
                                            certificate_id=args.certificate_id)
    utils.print_dict(val)


@utils.arg('listener_id', metavar='<LISTENER_ID>', type=str, help='ID of ELB Listener')
@utils.arg('--alg', metavar='<ALG>', type=str, help="Forwarding strategy, select in ['wrr', 'rr']")
@utils.arg('--protocol', metavar='<PROTOCOL>', type=str, help="Forwarding protocol, select in ['TCP', 'HTTP', 'HTTPS']")
@utils.arg('--frontend_port', metavar='<FRONTEND_PORT>', type=int, help="External serve port")
@utils.arg('--backend_port', metavar='<BACKEND_PORT>', type=int, help="Backend forwarded port")
@utils.arg('--enablesessionsticky', action='store_true')
@utils.arg('--name', metavar='<LISTENDER_NAME>', type=str, help='Listenser name')
@utils.arg('--check_interval', metavar='<CHECK_INTERVAL>', type=int, default=5, help='Health check interval, default 5s')
@utils.arg('--check_rise', metavar='<CHECK_RISE>', type=int, help='Check failed times treat backend available')
@utils.arg('--check_fall', metavar='<CHECK_FALL>', type=int, help='Check failed times treat backend not available')
@utils.arg('--check_timeout', metavar='<CHECK_TIMEOUT>', type=int, default=3, help='Check timeout, default=3s')
@utils.arg('--domain', metavar='<DOMAIN>', type=str, help='Domain name corresponding to forwarding rules')
@utils.arg('--location', metavar='<LOCATION>', type=str, help='URL location corresponding to forwarding rules')
@utils.arg('--cookie_name', metavar='<COOKIENAME>', type=str, help='Cookie name keep in session')
@utils.arg('--check_url', metavar='<CHECK_URL>', type=str, help='Health check url')
@utils.arg('--session_mode', metavar='<SESSION_MODE>', type=str, help='Session keep mode')
@utils.arg('--session_timeout', metavar='<SESSION_TIMEOUT>', type=int, help='Session timeout')
@utils.arg('--certificate_id', metavar='<CERTIFICATEID>', type=str, help='Https certificate id')
def do_ConfigLoadBalancerListener(client, args):
    """ Create a ELB instance """
    val = client.ConfigLoadBalancerListener(args.listener_id, alg=args.alg,
                                            name=args.name, protocol=args.protocol,
                                            frontend_port=args.frontend_port,
                                            backend_port=args.backend_port,
                                            enablesessionsticky=args.enablesessionsticky,
                                            check_interval=args.check_interval,
                                            check_rise=args.check_rise,
                                            check_fall=args.check_fall,
                                            check_timeout=args.check_timeout,
                                            domain=args.domain, location=args.location,
                                            cookie_name=args.cookie_name,
                                            check_url=args.check_url,
                                            session_mode=args.session_mode,
                                            session_timeout=args.session_timeout,
                                            certificate_id=args.certificate_id)
    utils.print_dict(val)


@utils.arg('--id', metavar='<ID>', action='append', help='ID of LoadBalancerListener')
@utils.arg('--limit', metavar='<LIMIT>', type=int, help='Limit')
@utils.arg('--offset', metavar='<OFFSET>', type=int, help='Offset')
def do_DescribeLoadBalancerListeners(client, args):
    """ List all ELB instances """
    val = client.DescribeLoadBalancerListeners(args.id, args.limit, args.offset)
    utils.print_list(val, 'Listener')


@utils.arg('id', metavar='<ID>', type=str, help='ID of ELB listenser')
def do_DeleteLoadBalancerListener(client, args):
    """ Delete a ELB Listener """
    val = client.DeleteLoadBalancerListener(args.id)
    utils.print_dict(val)


@utils.arg('--name', metavar='<SERVER_CUSTOMIZE_NAME>', type=str, help='Server customize name')
@utils.arg('--listener_id', metavar='<LISTENER_ID>', type=str, required=True, help='ID of Listener')
@utils.arg('--server_id', metavar='<SERVER_ID>', type=str, required=True, help='ID of Server')
@utils.arg('--weight', metavar='<WEIGHT>', type=int, help='Weight of forwarding')
@utils.arg('--port', metavar='<FORWARD_PORT>', type=int, help='Change forward port')
def do_RegisterBackendWithListener(client, args):
    """ Register Listener Backend server """
    val = client.RegisterBackendWithListener(args.listener_id, args.server_id, args.name,
                                             weight=args.weight, port=args.port)
    utils.print_dict(val)


@utils.arg('--listener_id', metavar='<LISTENER_ID>', type=str, required=True, help='ID of listener')
@utils.arg('--id', metavar='<ID>', action='append', help='ID of Backend')
@utils.arg('--limit', metavar='<LIMIT>', type=int, help='Limit')
@utils.arg('--offset', metavar='<OFFSET>', type=int, help='Offset')
def do_DescribeListenerBackends(client, args):
    """ List all Backends of specify Listener """
    val = client.DescribeListenerBackends(args.listener_id, args.id, args.limit, args.offset)
    utils.print_list(val, 'Backend')


@utils.arg('id', metavar='<BACKEND_ID>', type=str, help='Listener Backend ID')
@utils.arg('--listener_id', metavar='<LISTENER_ID>', type=str, help='Change corresponding Listener')
@utils.arg('--weight', metavar='<WEIGHT>', type=int, help='Weight of forwarding')
@utils.arg('--port', metavar='<FORWARD_PORT>', type=int, help='Change forward port')
def do_ConfigListenerBackend(client, args):
    """ Config Listener Backend """
    val = client.ConfigListenerBackend(args.id, args.listener_id,
                                       weight=args.weight, port=args.port)
    utils.print_dict(val)


@utils.arg('id', metavar='<ID>', type=str, help='ID of Backend')
def do_DeregisterBackendWithListener(client, args):
    """ Delete a Listener Backend """
    val = client.DeregisterBackendWithListener(args.id)
    utils.print_dict(val)

"""
    DeepLearning API
"""
@utils.arg('--id', metavar='<ID>', action='append', help='ID of DLProject')
@utils.arg('--name', metavar='<NAME>', action='append', help='Name of DLProject')
@utils.arg('--limit', metavar='<LIMIT>', type=int, help='Limit')
@utils.arg('--offset', metavar='<OFFSET>', type=int, help='Offset')
@utils.arg('--filter', metavar='<FILTER>', action='append', help='Filter')
@utils.arg('--order_by', metavar='<ORDER_BY>', type=str, help='ORDER_BY')
@utils.arg('--order', metavar='<ORDER>', type=str,
           help='ORDER:["desc", "asc"]')
def do_DescribeDLProjects(client, args):
    """List all DeepLearningProjects."""
    val = client.DescribeDLProjects(args.id, args.name, utils.convert_filter(args.filter),
                           args.limit, args.offset, args.order_by, args.order)
    utils.print_list(val, 'DLProject')

@utils.arg('name', metavar='<DLProject_NAME>', type=str, help='NAME of DLProject')
@utils.arg('--desc', metavar='<DESCRIPTION>', type=str,
           help='DESCRIPTION')
def do_CreateDLProject(client, args):
    """Create a DLProject."""
    val = client.CreateDLProject(args.name, args.desc)
    utils.print_dict(val)

@utils.arg('id', metavar='<DLProjecID>', type=str, help='ID of DLProject')
def do_DeleteDLProject(client, args):
    """Delete the DLProject."""
    client.DeleteDLProject(args.id)

@utils.arg('id', metavar='<DLProjecID>', type=str, help='ID of DLProject')
@utils.arg('--name', metavar='<NAME>', required=True, help='Name of DLProject')
@utils.arg('--desc', metavar='<DESCRIPTION>', help='Description of DLProject')
def do_UpdateDLProject(client, args):
    """Update the DLProject."""
    val = client.UpdateDLProject(args.id, args.name, args.desc)
    utils.print_dict(val, 'DLProject')

@utils.arg('project_id', metavar='<DLProjectID>', type=str, help='ID of DLProject')
@utils.arg('name', metavar='<DLJobName>', type=str, help='Name of DLJob')
@utils.arg('--hardware_mode', metavar='<HardwareMode>', required=True, type=str, choices=['CPU-ONLY', 'CPU-GPU'],
           help='hardware mode of DLJob, choices in [CPU-ONLY, CPU-GPU]')
@utils.arg('--distributed', action='store_true', help='DLJob is distributed')
@utils.arg('--job_type', metavar='<JobType>', required=True, type=str, choices=['training', 'inference'],
           help='Job type, choices in [training, inference]')
@utils.arg('--code_source', metavar='<CodeSource>', required=True, type=str,
           help='path of source code')
@utils.arg('--with_tensorboard', action='store_true', help='DLJob requires tensorboard')
@utils.arg('--auto_start', action='store_true', help='start DLJob automatically after creation')
@utils.arg('--node_num', metavar='<NodeNum>', type=int,
           help='Number of Worker Nodes, required integer > 0 in distributed mode')
@utils.arg('--gpu_num', metavar='<GpuNum>', type=int,
           help='Number of GPUs per Worker Node, required integer > 0 in CPU-GPU mode')
@utils.arg('--code_main_file', metavar='<CodeMainFile>', type=str,
           help='code main file, required when code_source is in compressed format, like tar.gz, tgz, zip ...')
@utils.arg('--data_dir', metavar='<DataDir>', type=str,
           help='directory for data')
@utils.arg('--ckpt_dir', metavar='<CkptDir>', type=str,
           help='directory for checkpoint/model')
@utils.arg('--output_dir', metavar='<OutputDir>', type=str,
           help='directory for output, valid for inference jobtype')
@utils.arg('--cmdline_args', metavar='<CmdlineArgs>', action='append',
           help='extra comandline args, like foo=bar')
@utils.arg('--tensorboard_log_dir', metavar='<TensorboardLogDir>', type=str,
           help='directory for tensorboard events if any')
@utils.arg('--notice_uid', metavar='<NoticeUID>', type=int,
           help='Whom to notice when DLJob finished, -1 stands for Job Owner')
@utils.arg('--distribute_file', metavar='<DistributedFile>', action='append',
           help='distribute and cache file to worker nodes\' $PWD for the DLJob')
@utils.arg('--desc', metavar='<DESCRIPTION>', type=str,
           help='DESCRIPTION')
@utils.arg('--image_id', metavar='<ImageId>', type=str,
           help='Docker Image ID')
def do_CreateDLJob(client, args):
    """Create a DLJob."""
    val = client.CreateDLJob(args.project_id, args.name, args.hardware_mode,
                                args.distributed, args.job_type, args.code_source,
                                args.with_tensorboard, args.auto_start,
                                args.node_num, args.gpu_num, args.code_main_file,
                                args.data_dir, args.ckpt_dir, args.output_dir,
                                args.cmdline_args, args.tensorboard_log_dir,
                                args.notice_uid, args.distribute_file, args.desc, args.image_id)
    utils.print_dict(val)

@utils.arg('project_id', metavar='<DLProjectID>', type=str, help='ID of DLProject')
@utils.arg('--id', metavar='<ID>', action='append', help='ID of DLJob')
@utils.arg('--name', metavar='<NAME>', action='append', help='Name of DLJob')
@utils.arg('--limit', metavar='<LIMIT>', type=int, help='Limit')
@utils.arg('--offset', metavar='<OFFSET>', type=int, help='Offset')
@utils.arg('--filter', metavar='<FILTER>', action='append', help='Filter')
@utils.arg('--order_by', metavar='<ORDER_BY>', type=str, help='ORDER_BY')
@utils.arg('--order', metavar='<ORDER>', type=str,
           help='ORDER:["desc", "asc"]')
def do_DescribeDLJobs(client, args):
    """List all DeepLearningJobs of a DLProject."""
    val = client.DescribeDLJobs(args.project_id, args.id, args.name, utils.convert_filter(args.filter),
                           args.limit, args.offset, args.order_by, args.order)
    utils.print_list(val, 'DLJob')

@utils.arg('id', metavar='<DLJobID>', type=str, help='ID of DLJob')
def do_DeleteDLJob(client, args):
    """Delete the DLJob."""
    client.DeleteDLJob(args.id)

@utils.arg('id', metavar='<DLJobID>', type=str, help='ID of DLJob')
@utils.arg('--name', metavar='<DLJobName>', type=str, help='Name of DLJob')
@utils.arg('--hardware_mode', metavar='<HardwareMode>', type=str, choices=['CPU-ONLY', 'CPU-GPU'],
           help='hardware mode of DLJob')
@utils.arg('--distributed', action='store_true', help='DLJob is distributed')
@utils.arg('--job_type', metavar='<JobType>', type=str, choices=['training', 'inference'],
           help='Job type')
@utils.arg('--code_source', metavar='<CodeSource>', type=str,
           help='path of source code')
@utils.arg('--with_tensorboard', action='store_true', help='DLJob require tensorboard')
@utils.arg('--auto_start', action='store_true', help='start DLJob automatically after creation')
@utils.arg('--node_num', metavar='<NodeNum>', type=int,
           help='Number of Worker Nodes')
@utils.arg('--gpu_num', metavar='<GpuNum>', type=int,
           help='Number of GPUs per Worker Node')
@utils.arg('--code_main_file', metavar='<CodeMainFile>', type=str,
           help='code main file')
@utils.arg('--data_dir', metavar='<DataDir>', type=str,
           help='directory for data')
@utils.arg('--ckpt_dir', metavar='<CkptDir>', type=str,
           help='directory for checkpoint/model')
@utils.arg('--output_dir', metavar='<OutputDir>', type=str,
           help='directory for output')
@utils.arg('--cmdline_args', metavar='<CmdlineArgs>', action='append',
           help='extra comandline args, like foo=bar')
@utils.arg('--tensorboard_log_dir', metavar='<TensorboardLogDir>', type=str,
           help='directory for tensorboard events if any')
@utils.arg('--notice_uid', metavar='<NoticeUID>', type=int,
           help='Whom to notice when DLJob finished, -1 for Job Owner')
@utils.arg('--distribute_file', metavar='<DistributedFile>', action='append',
           help='distribute and cache file to worker nodes\' $PWD for the DLJob')
@utils.arg('--desc', metavar='<DESCRIPTION>', type=str,
           help='DESCRIPTION')
@utils.arg('--image_id', metavar='<ImageId>', type=str,
           help='Docker Image ID')
def do_UpdateDLJob(client, args):
    """Update a DLJob."""
    val = client.UpdateDLJob(args.id, args.name, args.hardware_mode,
                                args.distributed, args.job_type, args.code_source,
                                args.with_tensorboard, args.auto_start,
                                args.node_num, args.gpu_num, args.code_main_file,
                                args.data_dir, args.ckpt_dir, args.output_dir,
                                args.cmdline_args, args.tensorboard_log_dir,
                                args.notice_uid, args.distribute_file, args.desc, args.image_id)
    utils.print_dict(val)

@utils.arg('id', metavar='<DLJobID>', type=str, help='ID of DLJob')
def do_SubmitDLJob(client, args):
    """Submit the DLJob."""
    client.SubmitDLJob(args.id)

@utils.arg('id', metavar='<DLJobID>', type=str, help='ID of DLJob')
def do_StopDLJob(client, args):
    """Stop the DLJob."""
    client.StopDLJob(args.id)

@utils.arg('--id', metavar='<ID>', action='append', help='ID of DLImage')
@utils.arg('--name', metavar='<NAME>', action='append', help='Name of DLImage')
@utils.arg('--limit', metavar='<LIMIT>', type=int, help='Limit')
@utils.arg('--offset', metavar='<OFFSET>', type=int, help='Offset')
@utils.arg('--filter', metavar='<FILTER>', action='append', help='Filter')
@utils.arg('--order_by', metavar='<ORDER_BY>', type=str, help='ORDER_BY')
@utils.arg('--order', metavar='<ORDER>', type=str,
           help='ORDER:["desc", "asc"]')
def do_DescribeDLImages(client, args):
    """List all DeepLearningImages."""
    val = client.DescribeDLImages(args.id, args.name, utils.convert_filter(args.filter),
                           args.limit, args.offset, args.order_by, args.order)
    utils.print_list(val, 'DLImage')

@utils.arg('name', metavar='<DLProject_NAME>', type=str, help='NAME of DLImage')
@utils.arg('image_config', metavar='<ImageConfig>', type=str, help='Dockerfile str for DLImage')
@utils.arg('--desc', metavar='<DESCRIPTION>', type=str,
           help='DESCRIPTION')
def do_CreateDLImage(client, args):
    """Create a DLImage."""
    val = client.CreateDLImage(args.name, args.image_config, args.desc)
    utils.print_dict(val)

@utils.arg('id', metavar='<DLImageID>', type=str, help='ID of DLImage')
def do_DeleteDLImage(client, args):
    """Delete the DLImage."""
    client.DeleteDLImage(args.id)

@utils.arg('id', metavar='<DLImageID>', type=str, help='ID of DLImage')
@utils.arg('--name', metavar='<NAME>', required=True, help='Name of DLImage')
@utils.arg('--image_config', metavar='<ImageConfig>', required=True, help='Dockerfile str for DLImage')
@utils.arg('--desc', metavar='<DESCRIPTION>', help='Description of DLImage')
def do_UpdateDLImage(client, args):
    """Update the DLImage."""
    val = client.UpdateDLImage(args.id, args.name, args.image_config, args.desc)
    utils.print_dict(val, 'DLImage')
