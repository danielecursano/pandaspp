from setuptools import setup, find_packages

setup(
    name="pandaspp",
    version="0.1.0",
    description="Pandas DataFrame subclass with correlation-aware drop tracking.",
    author="Daniele Cursano",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.2.0"
    ],
    python_requires=">=3.9.4",
)
