from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="pyxterms",
    version="1.4",
    author="akamedagoat",
    author_email="akamecanic@gmail.com",
    description="A python module to customize terminal and add coloring.",
    url="https://github.com/lutherantz/pyxterms",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_data={
        "": ["README.md", "LICENSE.md"],
    },
)