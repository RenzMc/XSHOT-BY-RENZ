#!/usr/bin/env python3
"""
Setup script for XShot
"""

from setuptools import setup, find_packages
import os

# Read the requirements from requirements.txt
with open(os.path.join(os.path.dirname(__file__), "requirements.txt")) as f:
    requirements = f.read().splitlines()

# Read the long description from README.md
with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="xshot",
    version="1.0.0",
    description="Advanced Screenshot Enhancement Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="XShot Team",
    author_email="example@example.com",
    url="https://github.com/yourusername/xshot",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'xshot_py': ['assets/fonts/*']
    },
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "xshot=xshot_py.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Android",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Utilities",
        "Topic :: System :: Archiving :: Backup",
        "Topic :: Desktop Environment",
    ],
    python_requires=">=3.8",
)