from setuptools import setup, find_packages
import os

VERSION = '1.4'
DESCRIPTION = 'Facilitating the process to store JSON data'

with open("README.md", 'r') as r:
    long_description = r.read()

# Setting up
setup(
    name="jsondatasave",
    version=VERSION,
    author="YourAverageDev",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'JSON', 'Data Storage'],  # Adjusted the keywords to be more representative
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    license="MIT"
)
