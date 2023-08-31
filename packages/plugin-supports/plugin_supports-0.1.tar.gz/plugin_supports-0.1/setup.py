from setuptools import setup, find_packages

setup(
    name="plugin_supports",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "sqlalchemy==2.0.19",
        "fastapi==0.96.0",
        "starlette==0.27.0",
        "pydantic==1.10.12"
    ],
)