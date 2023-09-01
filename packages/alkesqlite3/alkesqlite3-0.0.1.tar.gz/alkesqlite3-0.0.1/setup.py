#   coding:utf-8
#   This file is part of Alkemiems.
#
#   Alkemiems is free software: you can redistribute it and/or modify
#   it under the terms of the MIT License.

__author__ = 'Guanjie Wang'
__email__ = "gjwang@buaa.edu.cn"
__version__ = 1.0
__init___date__ = "2023/07/13 16:51:51"
__maintainer__ = 'Guanjie Wang'
__update_date__ = '2023/07/13 07:56:57'

import os
from setuptools import find_packages, setup

NAME = 'alkesqlite3'
VERSION = '0.0.1'
DESCRIPTION = ''
README_FILE = os.path.join(os.path.dirname(__file__), 'README.md')
LONG_DESCRIPTION = open(README_FILE, encoding='utf-8').read()

# sqlite3 2.6.0
# sqlite 3.42.0

REQUIREMENTS = ['matfleet>0.0.7']

URL = "https://gitee.com/alkemie_gjwang/alkesqlite3"
AUTHOR = __author__
AUTHOR_EMAIL = __email__
LICENSE = 'MIT'
PACKAGES = find_packages()

PACKAGE_DATA = {}
ENTRY_POINTS = {
}


def setup_package():
    setup(
        name=NAME,
        version=VERSION,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        license=LICENSE,
        packages=find_packages(),
        package_data=PACKAGE_DATA,
        include_package_data=True,
        entry_points=ENTRY_POINTS,
        install_requires=REQUIREMENTS,
        cmdclass={},
        zip_safe=False,
        url=URL
    )


if __name__ == '__main__':
    setup_package()
