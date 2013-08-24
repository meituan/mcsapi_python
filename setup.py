import os
import sys
import setuptools

from mosclient.common import setuputils

requires = setuputils.parse_requirements()

setuptools.setup(
    name="python-mosclient",
    version='0.1.20130719',
    description="Client library for Meituan Cloud Platform EC2 API",
    url='http://wiki.sankuai.com/pages/viewpage.action?pageId=71732595',
    author='Qiu Jian',
    author_email='qiujian@meituan.com',
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
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
    }
)
