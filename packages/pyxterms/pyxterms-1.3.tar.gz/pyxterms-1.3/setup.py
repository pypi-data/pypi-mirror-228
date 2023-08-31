from setuptools import setup, find_packages

setup(
    name="pyxterms",
    version="1.3",
    author="akamedagoat",
    author_email="akamecanic@gmail.com",
    description="A python module to customize terminal and add coloring.",
    url="https://github.com/lutherantz/pyxterms",
    packages=find_packages(),
    package_data={
        "": ["README.md", "LICENSE.md"],
    },
)