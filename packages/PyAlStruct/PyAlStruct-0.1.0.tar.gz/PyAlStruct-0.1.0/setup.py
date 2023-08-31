from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='PyAlStruct',
    version='0.1.0',
    author='fathi',
    author_email='abdelmalek.fathi.2001@gmail.com',
    url='https://github.com/fathiabdelmalek/PyAlStruct',
    description='Implementation of data structures and algorithms in python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[
        'al_struct',
        'al_struct.utils',
        'al_struct.algorithms',
        'al_struct.data_structures',
        'al_struct.data_structures.lists'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
