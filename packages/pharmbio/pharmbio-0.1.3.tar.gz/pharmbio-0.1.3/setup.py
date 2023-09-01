from setuptools import setup, find_packages

setup(
    name="pharmbio",
    version="0.1.3",
    url="https://github.com/pharmbio/pharmbio_package",
    author="Nima Chamyani",
    author_email="nima.ch@gmail.com",
    description="This is a Python package for interacting with Pharmb.io routine analysis.",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "polars",
        "pyarrow",
        "sqlalchemy",
        "connectorx>=0.3.1",
        "psycopg2-binary",
        "plotly",
        "nbformat",
        "matplotlib",
        "scikit-learn",
        "tqdm"
    ],
)
