import sys
import pathlib

from setuptools import find_packages, setup

try:
    from pip.req import parse_requirements
except ImportError:
    from pip._internal.req import parse_requirements

WORK_DIR = pathlib.Path(__file__).parent

if sys.version_info < (3, 7):
    raise RuntimeError("aioqiwi is not compatible for version lower Python 3.7")


with open("README.rst", "r", encoding="utf-8") as f:
    description = f.read()


file = WORK_DIR / "requirements.txt"
cur_requirements = parse_requirements(file, session="cur_session")
requirements = [str(ir.req) for ir in cur_requirements]

setup(
    name="aioqiwi",
    version="0.0.0.a1",
    packages=find_packages(exclude=("examples.*", "docs")),
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
    install_requires=requirements,
    package_data={"": ["requirements.txt"]},
    include_package_data=False,
    keywords='qiwi.com api-wrapper api qiwi-api asyncio aiohttp server webhooks',
)
