# coding: utf-8

"""
    Seaplane Config

    Contact: support@seaplane.io
"""

from setuptools import setup, find_namespace_packages

NAME = "seaplane_framework.config"
VERSION = "0.0.4"

REQUIRES = [
    "PyYAML==6.0",
]

setup(
    name=NAME,
    version=VERSION,
    author="Seaplane IO, Inc.",
    author_email="support@seaplane.io",
    url="",
    keywords=["Seaplane", "Carrier API"],
    python_requires=">=3.7",
    install_requires=REQUIRES,
    packages=find_namespace_packages(
        include=["seaplane_framework.*"], exclude=["test", "tests"]
    ),
    include_package_data=True,
    license="Apache 2.0",
    description="",
    long_description="",
)
