# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="uestcct",
    version="0.0.1",
    description="export uestc course table to google calendar",
    long_description=open("README.md").read(),
    author="helloqiu",
    author_email="helloqiu95@gmail.com",
    url="https://github.com/helloqiu/uestc_course_table",
    packages=find_packages(),
    package_data={"main": ["secret.json"]},
    entry_points={
        "console_scripts": ["uestc=main.cli:main"],
    },
    include_package_data=True,
    install_requires=open("requirements.txt").readlines(),
    license="GPLv3",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3 :: Only"
    ]
)
