import setuptools
from pathlib import Path

setuptools.setup(
    name='llcp_env',
    version='4.0.1',
    description="A OpenAI Gym Env for gym",
    long_description=Path("README.md").read_text(),
    long_description_content="text/markdown",
    packages=setuptools.find_packages(include="llcp_env*"),
    install_requires=['gym']
)