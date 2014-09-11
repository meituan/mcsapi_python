import setuptools

from build_py import build_py
from mosclient.common import setuputils

requires = setuputils.parse_requirements()

import os

if os.geteuid() == 0:
    data_files=[('/etc/bash_completion.d/', ['tools/completion/bash/climos']),
                ('/etc/bash_completion.d/helpers', ['tools/completion/climos.options']),
                ('/usr/share/zsh/functions/Completion/Linux', ['tools/completion/zsh/_climos'])]
else:
    data_files=[]

setuptools.setup(
    name="python-mosclient",
    version='0.1.20140825',
    description="Client library for Meituan Cloud Platform EC2 API",
    url='https://mos.meituan.com/docs/index.html',
    author='Meituan Open Services',
    author_email='mos@meituan.com',
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    data_files=data_files,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires=requires,
    entry_points={
        'console_scripts': ['climos = mosclient.shell:main']
    },
    cmdclass={'build_py': build_py}
)
