"""
Command-line interface to the API server.
"""


import sys
import argparse
import logging

import client

from common import utils

import urllib2


class APIShell(object):

    def get_base_parser(self):
        parser = argparse.ArgumentParser(
            prog='climos',
            description=__doc__.strip(),
            epilog='See "climos help COMMAND" '
                   'for help on a specific command.',
            add_help=False,
            formatter_class=HelpFormatter,
        )

        parser.add_argument('-h', '--help',
            action='store_true',
            help=argparse.SUPPRESS,
        )

        parser.add_argument('--debug',
            default=False,
            action='store_true',
            help=argparse.SUPPRESS,
        )

        parser.add_argument('--timeout',
            default=60,
            help='Number of seconds to wait for a response'
        )

        parser.add_argument('--mos-access',
            default=utils.env('MOS_ACCESS'),
            help='MOS access key, defaults to env[MOS_ACCESS]'
        )

        parser.add_argument('--mos-secret',
            default=utils.env('MOS_SECRET'),
            help='MOS secret, defaults to env[MOS_SECRET]'
        )

        parser.add_argument('--mos-url',
            default=utils.env('MOS_URL'),
            help='MOS api URL'
        )

        parser.add_argument('--mos-api-version',
            default=utils.env('MOS_API_VERSION', default='1'),
            help='MOS api version, defaults to env[MOS_API_VERSION] or 1'
        )

        parser.add_argument('--format', choices=['xml', 'json'],
            default=utils.env('MOS_FORMAT', default='xml'),
            help='Required return content type'
        )

        return parser

    def get_subcommand_parser(self, version):
        parser = self.get_base_parser()

        self.subcommands = {}
        subparsers = parser.add_subparsers(metavar='<subcommand>')
        submodule = utils.import_versioned_module(version, 'shell')
        self._find_actions(subparsers, submodule)
        self._find_actions(subparsers, self)

        return parser

    def _find_actions(self, subparsers, actions_module):
        for attr in (a for a in dir(actions_module) if a.startswith('do_')):
            callback = getattr(actions_module, attr)
            if callable(callback):
                command = attr[3:].replace('_', '-')
                desc = callback.__doc__ or ''
                help = desc.strip().split('\n')[0]
                arguments = getattr(callback, 'arguments', [])

                subparser = subparsers.add_parser(command,
                    help=help,
                    description=desc,
                    add_help=False,
                    formatter_class=HelpFormatter,
                )
                subparser.add_argument('-h', '--help',
                    action='help',
                    help=argparse.SUPPRESS,
                )
                self.subcommands[command] = subparser
                _args = []
                for (args, kwargs) in arguments:
                    for item in args:
                        _args.append(item)
                    subparser.add_argument(*args, **kwargs)
                subparser.set_defaults(func=callback)
                #self.command_dict.setdefault(command, _args)

    def main(self, argv):
        parser = self.get_base_parser()
        (options, args) = parser.parse_known_args(argv)
        api_version = options.mos_api_version
        subcommand_parser = self.get_subcommand_parser(api_version)
        self.parser = subcommand_parser

        if options.help or not argv:
            self.do_help(options)
            return 0

        args = subcommand_parser.parse_args(argv)

        if args.func == self.do_help:
            self.do_help(args)
            # import cgi
            # for cmd in self.subcommands:
            #     # print cmd
            #     if cmd.endswith('Node') or 'ECS' in cmd:
            #         p = self.subcommands[cmd]
            #         h = p.format_help()
            #         splited = h.split('\n\n', 2)
            #         usage, text, options = [cgi.escape(s.strip()) for s in splited]
            #         usage = usage[len('usage: climc '):]
            #         fmt = """
            #                 <tr>
            #                   <td colspan="1"><pre>{usage}</pre></td>
            #                   <td colspan="1"><pre>{text}</pre></td>
            #                   <td colspan="1"><pre>{options}</pre></td>
            #                   <td colspan="1"></td>
            #                 </tr>
            #                 """
                    # print fmt.format(usage=usage, text=text, options=options)
            return 0

        if not args.mos_access:
            raise Exception('You must provide mos_access via '
                            'either --mos-access or env[MOS_ACCESS]')

        if not args.mos_secret:
            raise Exception('You must provide mos_secret via '
                            'either --mos-secret or env[MOS_SECRET]')

        if not args.mos_url:
            raise Exception('You must provide mos_url via '
                            'either --mos-url or env[MOS_URL]')

        if args.debug:
            logger = logging.getLogger()
            logger.setLevel(logging.DEBUG)
        clt = client.Client(api_version,
                            args.mos_access, args.mos_secret, args.mos_url,
                            format=args.format,
                            timeout=args.timeout,
                            debug=args.debug)

        try:
            args.func(clt, args)
        except Exception as e:
            if not isinstance(e, urllib2.HTTPError):
                print '%s: %s' % (e.__class__.__name__, e)
            else:
                print self.get_httperror(e, args.debug)
            sys.exit(-1)

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

    @utils.arg('command', metavar='<subcommand>', nargs='?',
               help='Display help for <subcommand>')
    def do_help(self, args):
        """
        Display help about this program or one of its subcommands.
        """
        if getattr(args, 'command', None):
            if args.command in self.subcommands:
                self.subcommands[args.command].print_help()
            else:
                raise Exception("'%s' is not a valid subcommand" %
                                       args.command)
        else:
            self.parser.print_help()


class HelpFormatter(argparse.HelpFormatter):
    def start_section(self, heading):
        # Title-case the headings
        heading = '%s%s' % (heading[0].upper(), heading[1:])
        super(HelpFormatter, self).start_section(heading)


def main():
    api_shell = APIShell()
    api_shell.main(sys.argv[1:])
