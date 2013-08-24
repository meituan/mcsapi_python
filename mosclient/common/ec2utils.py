import logging
import hashlib
import hmac
import base64
import urllib


class Ec2Signer(object):
    """Hacked up code from boto/connection.py"""

    def __init__(self, secret_key):
        secret_key = secret_key.encode()
        self.hmac = hmac.new(secret_key, digestmod=hashlib.sha1)
        if hashlib.sha256:
            self.hmac_256 = hmac.new(secret_key, digestmod=hashlib.sha256)

    def generate(self, credentials):
        """Generate auth string according to what SignatureVersion is given."""
        if credentials['params']['SignatureVersion'] == '0':
            return self._calc_signature_0(credentials['params'])
        if credentials['params']['SignatureVersion'] == '1':
            return self._calc_signature_1(credentials['params'])
        if credentials['params']['SignatureVersion'] == '2':
            return self._calc_signature_2(credentials['params'],
                                          credentials['verb'],
                                          credentials['host'],
                                          credentials['path'])
        raise Exception('Unknown Signature Version: %s' %
                        credentials['params']['SignatureVersion'])

    @staticmethod
    def _get_utf8_value(value):
        """Get the UTF8-encoded version of a value."""
        if not isinstance(value, str) and not isinstance(value, unicode):
            value = str(value)
        if isinstance(value, unicode):
            return value.encode('utf-8')
        else:
            return value

    def _calc_signature_0(self, params):
        """Generate AWS signature version 0 string."""
        s = params['Action'] + params['Timestamp']
        self.hmac.update(s)
        return base64.b64encode(self.hmac.digest())

    def _calc_signature_1(self, params):
        """Generate AWS signature version 1 string."""
        keys = params.keys()
        keys.sort(cmp=lambda x, y: cmp(x.lower(), y.lower()))
        for key in keys:
            self.hmac.update(key)
            val = self._get_utf8_value(params[key])
            self.hmac.update(val)
        return base64.b64encode(self.hmac.digest())

    def _calc_signature_2(self, params, verb, server_string, path):
        """Generate AWS signature version 2 string."""
        logging.debug('using _calc_signature_2')
        string_to_sign = '%s\n%s\n%s\n' % (verb, server_string, path)
        if self.hmac_256:
            current_hmac = self.hmac_256
            params['SignatureMethod'] = 'HmacSHA256'
        else:
            current_hmac = self.hmac
            params['SignatureMethod'] = 'HmacSHA1'
        keys = params.keys()
        keys.sort()
        pairs = []
        for key in keys:
            val = self._get_utf8_value(params[key])
            val = urllib.quote(val, safe='-_~')
            pairs.append(urllib.quote(key, safe='') + '=' + val)
        qs = '&'.join(pairs)
        logging.debug('query string: %s', qs)
        string_to_sign += qs
        logging.debug('string_to_sign: %s', string_to_sign)
        current_hmac.update(string_to_sign)
        b64 = base64.b64encode(current_hmac.digest())
        logging.debug('len(b64)=%d', len(b64))
        logging.debug('base64 encoded digest: %s', b64)
        return b64
