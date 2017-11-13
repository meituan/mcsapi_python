import setuptools

from mosclient.common import setuputils

requires = setuputils.parse_requirements()

def read(path):
    with open(path, 'r') as f:
        return f.read()

setuptools.setup(
    name="mosclient",
    version='1.0.13',
    description="Client library for Meituan Cloud Platform EC2 API",

    long_description = (read('README.rst') + '\n\n' +
                        read('CHANGELOG.rst')),

    url='https://mos.meituan.com/document#sdk.html',
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
