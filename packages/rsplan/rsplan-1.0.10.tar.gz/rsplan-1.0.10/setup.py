# setup.py

import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "rsplan",
    version = "1.0.10",
    author = "Built Robotics",
    author_email = "engineering@builtrobotics.com",
    description = ("Reeds-Shepp algorithm implementation in Python."),
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    license = "MIT",
    keywords = "reeds-shepp path planning",
    url = "https://github.com/builtrobotics/rsplan",
    packages=['rsplan'],
    package_data={"rsplan": ["py.typed"]},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
)
