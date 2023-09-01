# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Copyright © 2023, Tiarnach Ó Riada
#
# Licensed under the terms of the Apache Software License 2.0
# ----------------------------------------------------------------------------
"""
PyGMID Plugin setup.
"""
from setuptools import find_packages
from setuptools import setup

from spyder_pygmid import __version__


setup(
    # See: https://setuptools.readthedocs.io/en/latest/setuptools.html
    name="spyder_pygmid",
    version=__version__,
    author="Tiarnach Ó Riada",
    author_email="tiarnach.oriada@tyndall.ie",
    description="Use PyGMID sweep and lookup within spyder",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license="Apache Software License 2.0",
    url="https://github.com/ollghra/pygmid-plugin",
    python_requires='>= 3.7',
    install_requires=[
        "pygmid",
        "qtpy",
        "qtawesome",
        "spyder>=5.0.1",
    ],
    packages=find_packages(),
    entry_points={
        "spyder.plugins": [
            "spyder_pygmid = spyder_pygmid.spyder.plugin:PyGMIDPlugin"
        ],
    },
    classifiers=[
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering",
    ],
)
