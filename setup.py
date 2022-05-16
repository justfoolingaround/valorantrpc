from setuptools import setup, find_packages
from valorantrpc.cli.__core__ import __version__

with open("requirements.txt", "r") as requirements_file:
    requirements = [_.strip() for _ in requirements_file.readlines()]


setup(
    name="valorantrpc",
    version=__version__,
    author="kr@justfoolingaround",
    author_email="kr.justfoolingaround@gmail.com",
    description="Damn, a great VALORANT RPC client.",
    packages=find_packages(),
    url="https://github.com/justfoolingaround/valorantrpc",
    install_requires=requirements,
    entry_points="""
        [console_scripts]
        valorantrpc=valorantrpc.__main__:valorant_rpc
    """,
)
