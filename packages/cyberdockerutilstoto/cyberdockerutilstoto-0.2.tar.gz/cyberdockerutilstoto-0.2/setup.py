from setuptools import setup, find_packages

# Read the contents of README file
with open("cyberdockerutilstoto/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='cyberdockerutilstoto',
    long_description=long_description,
    long_description_content_type="text/markdown",
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'PyYAML',
    ],
)
