from setuptools import setup


setup(
    name='Pastor',
    version='0.1.4',
    packages=['pastor'],
    description='Data store for Pandas.',
    url='https://github.com/rfow/pastor',
    license='LICENSE.txt',
    install_requires=['pandas', 'feather-format', 'orjson'],
)
