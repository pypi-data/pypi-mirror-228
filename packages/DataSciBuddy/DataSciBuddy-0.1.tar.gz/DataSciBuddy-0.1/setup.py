from setuptools import setup, find_packages

setup(
    name="DataSciBuddy",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas'
    ],
    author="Nicholas Karlson",
    author_email="NicholasKarlson@gmail.com",
    description="A data science helper package with datasets and utilities.",
    url="https://github.com/nicholaskarlson/DataSciBuddy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
