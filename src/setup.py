import os

from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))

install_requires = (
    "argparse",
    "six>=1.10.0",
)

setup(
    name='cmdtree',
    version='0.0.5',
    packages=find_packages(HERE, include=['cmdtree']),
    install_requires=install_requires,
    url='https://github.com/winkidney/cmdtree',
    license='MIT',
    author='winkidney',
    author_email='winkidney@gmail.com',
    description='Yet another cli tool library ,'
                'sub-command friendly, '
                'designed for cli auto-generating.',
)
