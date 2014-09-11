import sys
from setuptools.command.build_py import build_py as _build_py

class build_py(_build_py):
    def run(self):
        if not self.dry_run:
            # Generate climos completion options
            api_shell = CommandOptions()
            opts = api_shell.get_options()
            fp = open('tools/completion/climos.options', 'w')
            for key in opts.keys():
                one_cmd = str(key) + '# ' + ' '.join(opts[key])+'\n'
                fp.writelines(one_cmd)
            fp.close()
        _build_py.run(self)

class CommandOptions(object):
    def __init__(self):
        self.command_dict = {}

    def get_options(self):
        submodule = self.import_versioned_module('1', 'shell')
        self._find_actions(submodule)
        self._find_actions(self)
        return self.command_dict

    def import_versioned_module(self, version, submodule):
        module = 'mosclient.v%s' % version
        if submodule:
            module = '.'.join((module, submodule))
        return self.import_module(module)

    def import_module(self, import_str):
        __import__(import_str)
        return sys.modules[import_str]

    def _find_actions(self, actions_module):
        for attr in (a for a in dir(actions_module) if a.startswith('do_')):
            command = attr[3:].replace('_', '-')
            callback = getattr(actions_module, attr)
            arguments = getattr(callback, 'arguments', [])
            _args = []
            for (args, kwargs) in arguments:
                for item in args:
                    _args.append(item)
            self.command_dict.setdefault(command, _args)
