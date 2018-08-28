from setuptools import setup, find_packages

setup(
    name="sql-mojo-parser",
    version="0.0.6",
    install_requires=[
        "ply",
    ],
    author="L3viathan",
    author_email="git@l3vi.de",
    description="A lax parser for sql-like statements",
    url="https://github.com/L3viathan/sql-mojo-parser",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Intended Audience :: Developers",
    ],
)
