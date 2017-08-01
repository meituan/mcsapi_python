import sys
import os
import prettytable
import urllib
from functools import wraps


# Decorator for cli-args
def arg(*args, **kwargs):
    def _decorator(func):
        # Because of the sematics of decorator composition if we just append
        # to the options list positional options will appear to be backwards.
        func.__dict__.setdefault('arguments', []).insert(0, (args, kwargs))
        return func
    return _decorator


def get_value_ignorecase(dictobj, key):
    for k in dictobj.keys():
        if k.lower() == key.lower():
            return dictobj[k]
    return None


def get_attribute_ignorecase(obj, key):
    for a in obj.__dict__:
        if a.lower() == key().lower():
            return getattr(obj, a, None)
    return None


def print_list(data, field, fields=None, formatters={}):
    if isinstance(data, list):
        objs = data
        if len(objs) > 1:
            title = 'Total: %d' % len(objs)
        else:
            title = None
    elif isinstance(data, dict):
        objs = data.get(field, [])
        if not isinstance(objs, list):
            objs = [objs]
        total = int(data.get('Total', len(objs)))
        limit = int(data.get('Limit', 0))
        offset = int(data.get('Offset', 0))
        if limit > 0:
            pages = int(total)/limit
            if pages*limit < total:
                pages += 1
            page = (offset/limit) + 1
            title = 'Total: %d Pages: %d Limit: %d Offset: %d Page: %d' % \
                    (int(total), pages, limit, offset, page)
        else:
            title = 'Total: %d' % len(objs)
    else:
        objs = []
        title = 'Total: 0'
    if fields is None or len(fields) == 0:
        fields = []
        for o in objs:
            for k in o.keys():
                k = k.upper()
                if k not in fields:
                    fields.append(k)
    pt = prettytable.PrettyTable(fields, caching=False)
    pt.align = 'l'
    data_fields_tbl = {}
    for o in objs:
        row = []
        for field in fields:
            if field in formatters:
                row.append(formatters[field](o))
            else:
                field_name = field.lower().replace(' ', '_')
                if isinstance(o, dict):
                    data = get_value_ignorecase(o, field_name)
                else:
                    data = get_attribute_ignorecase(o, field_name)
                if data is None:
                    data = ''
                elif field not in data_fields_tbl:
                    data_fields_tbl[field] = True
                row.append(data)
        pt.add_row(row)

    data_fields = [f for f in fields if f in data_fields_tbl]
    print pt.get_string(fields=data_fields) #sortby=fields[0])
    if title is not None:
        print '****', title, '****'


def print_dict(d, key=None):
    pt = prettytable.PrettyTable(['Property', 'Value'], caching=False)
    pt.aligns = ['l', 'l']
    if not isinstance(d, dict):
        if key is not None:
            d = getattr(d, key, {})
        dd = {}
        for k in d.__dict__.keys():
            if k[0] != '_':
                v = getattr(d, k)
                if not callable(v):
                    dd[k] = v
        d = dd
    else:
        if key is not None:
            d = d.get(key, {})
    for r in d.iteritems():
        row = list(r)
        pt.add_row(row)
    print pt.get_string(sortby='Property')


def string_to_bool(arg):
    return arg.strip().lower() in ('t', 'true', 'yes', '1')


def env(*vars, **kwargs):
    """Search for the first defined of possibly many env vars

    Returns the first environment variable defined in vars, or
    returns the default defined in kwargs.
    """
    for v in vars:
        value = os.environ.get(v, None)
        if value:
            return value
    return kwargs.get('default', '')


def import_module(import_str):
    """Import a module."""
    __import__(import_str)
    return sys.modules[import_str]


def import_versioned_module(version, submodule=None):
    module = 'mosclient.v%s' % version
    if submodule:
        module = '.'.join((module, submodule))
    return import_module(module)


def urlencode(data):
    assert(isinstance(data, dict))
    kw_list = []
    for k in data.keys():
        if data[k] is not None:
            if isinstance(data[k], list):
                for v in data[k]:
                    kw_list.append({k: v})
            else:
                kw_list.append({k: data[k]})
    kw_list = sorted(kw_list, lambda x, y: cmp(x.keys()[0], y.keys()[0]))
    return '&'.join(map(urllib.urlencode, kw_list))


def decrypt(privkey, secret):
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_OAEP
    key = RSA.importKey(privkey)
    cipher = PKCS1_OAEP.new(key)
    message = cipher.decrypt(secret)
    return message

def decrypt_base64(privkey, secret):
    import base64
    return decrypt(privkey, base64.b64decode(secret))


def parse_isotime(expires):
    from datetime import datetime
    return datetime.strptime(expires+"UTC", '%Y-%m-%dT%H:%M:%SZ%Z')


def get_paging_info(args):
    info = {}
    if args.limit:
        info['limit'] = int(args.limit)
    if args.offset:
        info['offset'] = int(args.offset)
    if args.order_by:
        info['order_by'] = args.order_by
        if args.order:
            info['order'] = args.order
    if args.details:
        info['details'] = True
    else:
        info['details'] = False
    if args.search:
        info['search'] = args.search
    if getattr(args, 'admin', False):
        info['admin'] = True
    tenant = getattr(args, 'tenant', None)
    if tenant is not None:
        info['admin'] = True
        info['tenant'] = tenant
    return info


def md5sum(filename):
    import hashlib
    md5 = hashlib.md5()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(128*md5.block_size), b''):
            md5.update(chunk)
    return md5.hexdigest()


def ensure_unicode(s):
    if not isinstance(s, basestring):
        s = '%s' % s
    if isinstance(s, unicode):
        return s
    else:
        return s.decode('utf-8')


def ensure_ascii(s):
    if not isinstance(s, basestring):
        s = '%s' % s
    if isinstance(s, str):
        return s
    else:
        return s.encode('utf-8')


def ensure_bool(s):
    if isinstance(s, bool):
        return s
    elif isinstance(s, int) or isinstance(s, float):
        if s > 0:
            return True
        else:
            return False
    else:
        if not isinstance(s, basestring):
            s = '%s' % s
        if s.lower() in ['true', 'yes', '1']:
            return True
        else:
            return False


def url_quote(s):
    return urllib.quote(s)


def url_join(*args):
    args = map(ensure_ascii, args)
    args = map(urllib.quote, args)
    return '/'.join(args)


def convert_filter(filters):
    if isinstance(filters, list) and len(filters) > 0:
        filter_dict = {}
        for f in filters:
            dat = f.split(':')
            if len(dat) >= 2:
                filter_dict[dat[0]] = dat[1:]
        return filter_dict
    return None


def get_page_info(args):
    kwargs = {}
    if getattr(args, 'limit', 0) > 0:
        kwargs['Limit'] = args.limit
    if int(getattr(args, 'offset', 0)) > 0:
        kwargs['Offset'] = args.offset
    if getattr(args, 'filter', None) and len(args.filter) > 0:
        idx = 1
        for f in args.filter:
            dat = f.split(':')
            if len(dat) >= 2:
                kwargs['Filter.%d.Name' % idx] = dat[0]
                vidx = 1
                for v in dat[1:]:
                    kwargs['Filter.%d.Value.%d' % (idx, vidx)] = v
                    vidx += 1
            idx += 1
    return kwargs


# Decorator for get http error or expected success response to prettytable print
def expect(expected_key):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            val = func(*args, **kwargs)
            if 'code' in val or 'err' in val:
                return val
            else:
                return val[expected_key]
        return wrapper
    return decorator
