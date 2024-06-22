# -*- coding: utf-8 -*-
# ****************************************************************
# aitk.algorithms: Algorithms for AI
#
# Copyright (c) 2021 AITK Developers
#
# https://github.com/ArtificialIntelligenceToolkit/aitk.algorithms
#
# ****************************************************************

import setuptools

name = "aitk.algorithms"
version = "2.0.0"
long_description = """
# aitk.algorithms

DEPRECATED PACKAGE: use `aitk` instead.
"""
print(long_description)
setup_args = dict(
    name=name,
    version=version,
    url="https://github.com/ArtificialIntelligenceToolkit/%s" % name,
    author="Lisa Meeden",
    description="General Algorithms for AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["aitk"],
    python_requires=">=3.6",
    license="BSD-3-Clause",
    platforms="Linux, Mac OS X, Windows",
    keywords=["ai", "algorithms", "python"],
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)

if __name__ == "__main__":
    setuptools.setup(**setup_args)
