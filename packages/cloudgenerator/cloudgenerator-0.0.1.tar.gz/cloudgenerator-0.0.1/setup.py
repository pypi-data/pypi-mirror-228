from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A safe genetator'

# Setting up
setup(
    name="cloudgenerator",
    version=VERSION,
    author="NoticedCloud",
    author_email="noticedcloud@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=["Cryptodome"],
    keywords=['python', 'password', 'token', 'safe'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)