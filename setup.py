import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="digikey-api",
    version="0.6.1",
    author="Peter Oostewechel",
    author_email="peter_oostewechel@hotmail.com",
    license="GPL v3",
    url="https://github.com/peeter123/digikey-api",
    description="Python client for Digikey API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=['contrib', 'docs', 'tests']),
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development",
    ],
    install_requires=[
        'requests>=2.22.0',
        'retrying>=1.3.3',
        'schematics>=2.1.0',
        'inflection>=0.3.1',
        'certauth>=1.3.0',
        'urllib3>=1.25.3'
    ],
    tests_requires=['pytest>=5.1.2'],
)
