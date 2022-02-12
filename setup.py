from setuptools import setup


setup(
    name="zenodozen",
    version="0.1a1",
    description="A client for the zenodo API",
    author="Jonah Kanner",
    url="https://github.com/jkanner/zenodozen",
    py_modules=["zenodozen"],
    install_requires=[
        "requests",
    ],
)
