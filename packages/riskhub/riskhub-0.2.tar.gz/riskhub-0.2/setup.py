#! /usr/bin/python
# coding: utf-8
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setup(
    name="riskhub",
    version="0.2",
    author='sabarish',
    author_email="sabarishbugbounty@gmail.com",
    description="fetching URLs to any domains",
    packages=find_packages(),
    install_requires=[
        'requests==2.27.1',
        'argparse==1.4.0',
        'apscheduler==3.9.1',
        'urllib3==1.24.2',
        'APScheduler==3.9.1',
        'httplib2==0.22.0',
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points= {
        'console_scripts': [
            'riskhub=riskhub.riskhub:main',
        ],
    },
)