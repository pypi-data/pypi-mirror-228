from setuptools import setup, find_packages
import pathlib

CURRENT_DIR = pathlib.Path(__file__).parent

# The text of the README file
README = (CURRENT_DIR / "README.md").read_text(encoding="utf-8")

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="docsdb",
    author="deji",
    author_email="deji.a.ibrahim@gmail.com",
    version="0.1.7",
    description="docsdb - generate static documentation for your database",
    license="MIT",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "docsdb = docsdb.main:cli",
        ],
    },
)
