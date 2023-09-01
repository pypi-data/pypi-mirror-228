from setuptools import find_packages, setup

from yqf_test.test import version

setup(
    name="yqf_test",
    author="yqf",
    license="MIT",
    packages=find_packages("dynamic-ha/yqf_test"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    version=version,
    python_requires=">=3.7",
)