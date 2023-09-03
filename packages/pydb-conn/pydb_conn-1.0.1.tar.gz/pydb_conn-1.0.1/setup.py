from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pydb_conn",
    version="1.0.1",
    packages=find_packages(),
    author="Daniel Taiba",
    author_email="danielt.dtr@gmail.com",
    description="Python connector to Microsoft SQL Server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='DataFrame MsSQL',
    url='https://github.com/oym-tritec/pydb_conn',
    install_requires=[
        "numpy==1.25.2",
        "pandas==2.1.0",
        "pyodbc==4.0.39",
        "pytz==2023.3",
        "SQLAlchemy==2.0.20"
    ],
)
