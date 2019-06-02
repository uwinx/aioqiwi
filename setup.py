import pathlib
import re

from setuptools import find_packages, setup

WORK_DIR = pathlib.Path(__file__).parent

code = (WORK_DIR / 'aioqiwi' / '__init__.py').read_text('utf-8')
try:
    version = re.findall(r"^__version__ = '([^']+)'\r?$", code, re.M)[0]
except IndexError:
    raise RuntimeError('Unable to determine version.')


with open("readme.rst", "r", encoding="utf-8") as f:
    description = f.read()


setup(
    name="aioqiwi",
    version=version,
    packages=find_packages(exclude=("examples.*", "test.*", "docs", 'test')),
    url="https://github.com/uwinx/aioqiwi",
    license="MIT",
    author="pascal",
    requires_python=">=3.7",
    author_email="mpa@snejugal.ru",
    description="Async and convenient qiwi.com API wrapper",
    long_description=description,
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires='aiohttp>=3.5.4',
    package_data={"": ["requirements.txt"]},
    include_package_data=False,
    keywords='qiwi.com api-wrapper api qiwi-api asyncio aiohttp server webhooks',
)
