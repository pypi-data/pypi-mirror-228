import setuptools

with open("README.md", "r", encoding = "utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name = "pitters",
    version = "0.0.1",
    author = "Pedro Toledo",
    author_email = "ptoledor@msn.com",
    description = "Simple and useful functions for data analysis",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/ptoledor/pypi-pitters",
    license="MIT",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages = setuptools.find_packages(),
    install_requires=['pandas', 'numpy'], 
    python_requires = ">=3.6",
)
