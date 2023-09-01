# python setup.py install

from setuptools import setup, find_packages

setup(
    name="datapeach",
    version="1.0.1",
    py_modules=["datapeachcli"],
    package_data={"datapeach_cli": ["templates/*", "config.json"]},
    install_requires=[
        "click",
        "jinja2",
        "nbformat",
        "nbconvert",
        "pulsar",
        "mysql-connector",
        "pandas",
        "pyyaml",
        "ipython",
        "requests",
        "datapeach-wrapper",
    ],
    entry_points="""
        [console_scripts]
        datapeach=datapeachcli:cli
    """,
    packages=find_packages(),
)
