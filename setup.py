#!/usr/bin/env python

from setuptools import setup
import nonconformist

setup(
    name="cbl-nonconformist",
    packages=["nonconformist"],
    version=nonconformist.__version__,
    description="Python implementation of the conformal prediction framework.",
    author="Henrik Linusson",
    author_email="henrik.linusson@gmail.com",
    url="https://github.com/eloyfelix/cbl-nonconformist",
    download_url="",
    install_requires=["numpy", "scikit-learn>=0.20", "scipy", "pandas"],
    keywords=[
        "conformal prediction",
        "machine learning",
        "classification",
        "regression",
    ],
    classifiers=[
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Scientific/Engineering",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
    ],
)

# Authors: Henrik Linusson
