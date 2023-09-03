#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MoneyWorld",
    version="2023.9.1",
    author="anzechannel",
    author_email='348834851@qq.com',
    description="这是一个关于自动化交易的软件包",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
