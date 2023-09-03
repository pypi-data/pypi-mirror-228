from setuptools import setup, find_packages
from pathlib import Path

NAME = 'poethu'
VERSION = '1.0.4'
AUTHOR = 'BXn4 (Bence)'
LICENSE = 'MIT'
URL = 'https://github.com/bxn4/poethu'

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Setting up
setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    description='An unofficial Python wrapper for the poet.hu API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license=LICENSE,
    url=URL,
    keywords="python poet API",
    python_requires='>=3.0',
    packages=find_packages(),
    install_requires=['requests'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
