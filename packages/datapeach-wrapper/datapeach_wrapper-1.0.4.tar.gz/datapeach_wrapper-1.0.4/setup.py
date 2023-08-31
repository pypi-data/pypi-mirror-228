# setup.py

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    description = fh.read()

setup(
    name="datapeach_wrapper",
    version="1.0.4",
    author="datapeach",
    author_email="datapeach@gigarion.com",
    packages=find_packages(),
    description="datapeach wrapper",
    long_description=description,
    long_description_content_type="text/markdown",
    url="",
    license="MIT",
    python_requires=">=3.8",
    install_requires=[
        "nbformat",
        "nbconvert",
        "pulsar",
        "mysql.connector",
        "pandas",
        "pyyaml",
        "requests",
    ],
)
