import sys
import json
import urllib
import urllib2

from urlparse import urlparse
from datetime import datetime

import ec2utils
from xmltodict import parse


class BaseClient(object):

    def __init__(self, access, secret, url, format=None,
                 timeout=300, debug=False, region='Beijing'):
        self.access = access
        self.secret = secret
        self.url = url
        self.format = format
        self.timeout = timeout
        self.debug = debug
        self.region = region

    def _get_action(self, level):
        if getattr(sys, '_getframe', None) is not None:
            co = sys._getframe(level).f_code
            func = getattr(self, co.co_name, None)
            if func is not None and callable(func):
                return co.co_name
        else:
            raise Exception('Cannot retrieve action name on this platform')

    def get_signature(self, params):
        req = urlparse(self.url)
        host = req.netloc
        if (req.scheme == 'http' and host.endswith(':80')) or \
                (req.scheme == 'https' and host.endswith(':443')):
            host = host[:host.rfind(':')]
        path = req.path
        if req.path == '':
            path = '/'
        cred_dict = {
            'access': self.access,
            'host': host,
            'verb': 'POST',
            'path': path,
            'params': params,
        }
        signer = ec2utils.Ec2Signer(self.secret)
        return signer.generate(cred_dict)

    def get_httperror(self, e, debug):
        details = e.read()
        if debug:
            print details
        try:
            if 'application/xml' in e.headers.get('Content-Type', None):
                from common.xmltodict import parse
                details = parse(details)
            else:
                import json
                details = json.loads(details)
            if 'ErrorResponse' in details:
                details = details['ErrorResponse']
            if 'Error' in details:
                details = details['Error']
            if 'error' in details:
                details = details['error']
            if 'message' in details:
                details = details['message']
            elif 'details' in details:
                details = details['details']
        except:
            pass
        if not isinstance(details, basestring):
            details = str(details)
        return '%s(%d): %s' % (e.msg, e.code, details)


    def _request(self, **kwargs):
        params = {}
        params['Action'] = self._get_action(3)
        params['AWSAccessKeyId'] = self.access
        params['Timestamp'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z')
        params['SignatureVersion'] = '2'
        params['SignatureMethod'] = 'HmacSHA256'
        params['Region'] = self.region
        for k, v in kwargs.iteritems():
            if isinstance(v, list):
                i = 1
                for vi in v:
                    params['%s.%d' % (k, i)] = vi
                    i += 1
            else:
                params[k] = v
        if self.format:
            params['Format'] = self.format
        sig = self.get_signature(params)
        params['Signature'] = sig
        headers = {}
        headers['User-Agent'] = 'python-mosclient'
        data = urllib.urlencode(params)
        if self.debug:
            print self.url + '?' + data
        req = urllib2.Request(self.url, data, headers)

        try:
            resp = urllib2.urlopen(req, None, self.timeout)
            return resp
        except urllib2.HTTPError, e:
            print self.get_httperror(e, self.debug)
        except Exception, e:
            raise e


    def raw_request(self, **kwargs):
        return self._request(**kwargs)

    def request(self, **kwargs):
        resp = self._request(**kwargs)
        if not resp:
            return
        body = resp.read()
        if self.debug:
            print resp.headers
            print body
        try:
            if resp.headers['Content-Type'].startswith('application/json'):
                body = json.loads(body)
            else:
                body = parse(body)
            action = self._get_action(2)
            return body['%sResponse' % action]
        except:
            return body

    @classmethod
    def parse_list_params(self, limit, offset, filters, kwargs):
        if limit > 0:
            kwargs['Limit'] = limit
        if offset > 0:
            kwargs['Offset'] = offset
        if filters is not None:
            fidx = 1
            for k, vs in filters.iteritems():
                kwargs['Filter.%d.Name' % fidx] = k
                if not isinstance(vs, list):
                    vs = [vs]
                vidx = 1
                for v in vs:
                    kwargs['Filter.%d.Value.%d' % (fidx, vidx)] = v
                    vidx += 1
                fidx += 1
