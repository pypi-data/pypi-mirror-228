from setuptools import setup, find_packages

setup(
    name="autodropstack",
    version="0.1.1",
    description="filo stack",
    author="thearyadev",
    packages=find_packages(),
    package_data={"": ["*.txt", "*.md"]},
    long_description=open("README.md").read(),
)
