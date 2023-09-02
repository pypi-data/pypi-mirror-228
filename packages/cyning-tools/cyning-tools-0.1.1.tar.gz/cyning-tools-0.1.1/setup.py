#!/usr/bin/env python
# coding:utf8
# Cyning <zhixiao476@gmail.com>
# 2023/9/2 - 14:53
#

from setuptools import setup, find_packages

setup(
    name="cyning-tools",
    version='0.1.1',
    description="常用的工具类库",
    author="Cyning",
    author_email="zhixiao476@gmail.com",
    py_modules=['cytools'],
    #install_requires=['pymysql', 'tornado', 'aiofiles', 'aiohttp', 'aioredis', 'aiomysql']
    packages=find_packages(),
    install_requires=[]
)