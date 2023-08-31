from setuptools import setup, find_packages
import datetime

version = int(datetime.datetime.now().timestamp())

setup(
    name='bewe',
    version=f'0.1.2.{version}',
    description='The package implements some investment strategies.',
    long_description='Bewe.',
    author='Berlin Hsin',
    author_email='berlin.hsin@gmail.com',
    packages=find_packages(),
    install_requires=[
    ]
)
