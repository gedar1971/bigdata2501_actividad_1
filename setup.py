from setuptools import setup, find_packages

setup(
    name="bigdata_actividad_1",
    version="0.0.1",
    author="German Arbelaez",
    author_email="",
    description="",
    py_modules=["actividad_1"],
    install_requires=[
        "pandas",
        "openpyxl",
        "requests",
        "sqlite3",
        "os"
    ] 
)