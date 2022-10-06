#!/usr/bin/python3
import re
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kicost_digikey_api_v3",
    version="0.1.2",
    author="Salvador E. Tropea",
    author_email="stropea@inti.gob.ar",
    license="GPL v3",
    url="https://github.com/set-soft/kicost-digikey-api-v3",
    description="KiCost plugin for the Digikey PartSearch API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=['contrib', 'docs', 'tests']),
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development",
    ],
    install_requires=[
        'inflection>=0.3.1',
        'requests>=2.21',
        'urllib3>=1.24',
        'six',
        'certifi',
        'setuptools',
        'pyopenssl',
        'tldextract',
        'python-dateutil'],
    tests_requires=['pytest>=5.1.2'],
)