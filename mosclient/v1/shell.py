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
@utils.arg('--datadisk', metavar='<DISKSIZE>', type=int, help='Extra disksize in GB')
@utils.arg('--bandwidth', metavar='<BANDWIDTH>', type=int, help='Extra external bandwidth in Mbps')
def do_CreateInstance(client, args):
    """ Create servers """
    val = client.CreateInstance(args.image, args.instance_type,
                                duration=args.duration,
                                name=args.name,
                                keypair=args.keypair,
                                datadisk=args.datadisk,
                                bandwidth=args.bandwidth)
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
@utils.arg('--limit', metavar='<LIMIT>', type=int, help='Limit')
@utils.arg('--offset', metavar='<OFFSET>', type=int, help='Limit')
@utils.arg('--filter', metavar='<FILTER>', action='append', help='Filter')
def do_DescribeInstances(client, args):
    """ Get details of all or specified instances """
    val = client.DescribeInstances(args.id, args.name, args.limit, args.offset, utils.convert_filter(args.filter))
    utils.print_list(val, 'Instance')


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
@utils.arg('--force', action='store_true', help='Force stop running isntance')
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
