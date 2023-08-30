import os

from setuptools import setup, find_packages


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="pynubankasync",
    version="2.25.1",
    url="https://github.com/humbertogontijo/pynubankasync",
    author="André Roggeri Campos",
    author_email="a.roggeri.c@gmail.com",
    license="MIT",
    packages=find_packages(),
    package_data={"pynubankasync": ["queries/*.gql", "utils/mocked_responses/*.json"]},
    install_requires=required,
    setup_requires=["pytest-runner"],
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    entry_points={"console_scripts": ["pynubankasync = pynubankasync.cli:main"]},
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
