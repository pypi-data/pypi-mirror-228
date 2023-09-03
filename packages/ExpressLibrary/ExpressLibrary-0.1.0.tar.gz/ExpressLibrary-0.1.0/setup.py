from setuptools import setup, find_packages

# Read the content of the README.md file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='ExpressLibrary',
    version='0.1.0',
    url='https://github.com/shahid265/ExpressLibrary.git',
    author='Shahid',
    author_email='shahid265.sr@gmail.com',
    description='Express library is a Python package designed to streamline the data visualization process in a consultancy environment. This package aims to facilitate the quick transformation of data into insightful visualizations. It is developed on top of standard libraries such as Plotly and Circlify.',
    packages=find_packages(),    
    install_requires=['plotly', 'pandas', 'circlify', 'matplotlib', 'pytest'],
    long_description=long_description,
    long_description_content_type="text/markdown",
)