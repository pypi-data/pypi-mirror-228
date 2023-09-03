import os
from setuptools import setup
from setuptools import find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()


VERSION = '0.1.1'

setup(
    name='wqtool',  # package name
    version=VERSION,  # package version
    description='wuqi tool',  # package description
    author='deng.weiwei',
    author_email='deng.weiwei@wuqi-tech.com',
    install_requires=['Scons'],
    long_description=README,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.8',
    ],
    packages=find_packages(),
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'wqtool = src.wqtool:main',
        ],
    }
)