from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()


setup(
    name = 'bitex-blockchain-explorer',
    version = '0.1.1',
    author = 'Nika Kudukhashvili',
    author_email = 'nikakuduxashvili0@gmail.com',
    description = 'A Python module for interacting with blockchain data using the Bitex blockchain explorer',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/Kuduxaaa/bitex-blockchain-explorer',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
