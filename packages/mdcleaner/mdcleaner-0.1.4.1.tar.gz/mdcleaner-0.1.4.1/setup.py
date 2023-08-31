from setuptools import setup, find_packages

# Read the content of the README.md file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mdcleaner",
    version="0.1.4.1",
    packages=find_packages(),
    description="A utility to clean and convert MD files to ASCII.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "chardet",
        "unidecode"
    ],
    author="Devon White",
    author_email="devon.white@signalwire.com",
    license="MIT",
    keywords="markdown cleaner ASCII",
    python_requires='>=3.6',  # if you want to specify a minimum Python version
)
