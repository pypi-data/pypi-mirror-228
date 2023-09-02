#!/usr/bin/env python
"""Python log parser for ULog.

This module allows you to parse ULog files, which are used within the PX4
autopilot middleware.

The file format is documented on https://docs.px4.io/master/en/dev_log/ulog_file_format.html

"""

from __future__ import print_function
import os
import sys
# import versioneer

from setuptools import setup, find_packages

DOCLINES = __doc__.split("\n")

CLASSIFIERS = """\
Development Status :: 1 - Planning
Intended Audience :: Science/Research
Intended Audience :: Developers
License :: OSI Approved :: BSD License
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Other
Topic :: Software Development
Topic :: Scientific/Engineering :: Artificial Intelligence
Topic :: Scientific/Engineering :: Mathematics
Topic :: Scientific/Engineering :: Physics
Operating System :: Microsoft :: Windows
Operating System :: POSIX
Operating System :: Unix
Operating System :: MacOS
"""

# pylint: disable=invalid-name

setup(
    name='pysulog',
    maintainer="Your Name",
    maintainer_email="your.email@example.com",
    description=DOCLINES[0],
    long_description="\n".join(DOCLINES[2:]),
    url='https://github.com/yourusername/pyulog',
    author='Your Name',
    author_email='your.email@example.com',
    download_url='https://github.com/yourusername/pyulog',
    license='BSD 3-Clause',
    classifiers=[_f for _f in CLASSIFIERS.split('\n') if _f],
    platforms=["Windows", "Linux", "Solaris", "Mac OS-X", "Unix"],
    install_requires=['numpy'],
    tests_require=['pytest', 'ddt'],
    entry_points = {
        'console_scripts': [
            # 添加或修改需要的命令行工具
        ],
    },
    packages=find_packages(),
    version= '1.0.3',
    include_package_data=True,
)
