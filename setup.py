from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name="piedb",
    version="0.1.0",
    author="Shubham Kumar Gupta",
    author_email="skgsmasher14243@gmail.com",
    description="A lightweight JSON-based database",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/shubham14243/piedb",
    packages=find_packages(),
    install_requires=[],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
