from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="PyGptRes",
    version="2.0",
    author="akamedagoat",
    author_email="akamecanic@gmail.com",
    description="PyGptRes is a Python module for interacting with OpenAI's GPT-3.5 Turbo API to create natural language conversations with cutting-edge language models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lutherantz/pygptres",
    packages=find_packages(),
)