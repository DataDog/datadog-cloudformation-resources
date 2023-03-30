from setuptools import setup

version = {}
with open("src/datadog_cloudformation_common/version.py") as fp:
    exec(fp.read(), version)

setup(version=version["__version__"])
