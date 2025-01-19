# setup.py
from setuptools import setup, find_packages

setup(
    name="llmtools",            # Package name
    version="0.0.1",                # Version number
    packages=find_packages(),     # Automatically find packages in the directory
    install_requires=[],          # List dependencies if any
    author="rainfishs",           # Your name
    author_email="rainfish122456@gmail.com",  # Your email
    description="A simple Python package",  # Short description
    long_description=open('README.md').read(),  # Detailed description from README
    long_description_content_type="text/markdown",
    url="https://github.com/rainfishs/llmtools",  # GitHub URL
    classifiers=[                # Classifiers for the package
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
