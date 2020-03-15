from setuptools import find_packages, setup


with open("readme.rst", "r", encoding="utf-8") as f:
    description = f.read()


setup(
    name="aioqiwi",
    version="1.1.0",
    packages=find_packages(exclude=("examples.*", "test.*", "docs", "test")),
    url="https://github.com/uwinx/aioqiwi",
    license="MIT",
    author="Martin Winks",
    requires_python=">=3.7",
    author_email="mpa@snejugal.ru",
    description="Async and convenient qiwi.com API wrapper",
    long_description=description,
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=["aiohttp>=3.6.2", 'pydantic>=1.4'],
    include_package_data=False,
    keywords="qiwi.com api-wrapper qiwi-api aiohttp server webhooks",
)
