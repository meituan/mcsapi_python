import setuptools

from mosclient.common import setuputils

requires = setuputils.parse_requirements()

setuptools.setup(
    name="python-mosclient",
    version='1.0.3',
    description="Client library for Meituan Cloud Platform EC2 API",
    url='https://mos.meituan.com/docs/index.html',
    author='Meituan Open Services',
    author_email='mos@meituan.com',
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
