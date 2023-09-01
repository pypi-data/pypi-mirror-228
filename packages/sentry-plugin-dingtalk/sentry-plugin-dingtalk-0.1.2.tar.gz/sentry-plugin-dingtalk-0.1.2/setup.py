#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

setup(
    name="sentry-plugin-dingtalk",
    version='0.1.2',
    author='ding',
    author_email='ding@ding.com',
    description='A Sentry extension which send errors stats to dingtalk',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    keywords='sentry dingtalk',
    include_package_data=True,
    zip_safe=False,
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        'sentry>=9.0.0',
        'requests',
    ],
    entry_points={
        'sentry.plugins': [
            'sentry_plugin_dingtalk = sentry_plugin_dingtalk.plugin:dingtalkPlugin'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License",
    ]
)
