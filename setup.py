from setuptools import setup

setup(
    name="qomma",
    version="0.1.0",
    packages=["qomma"],
    entry_points={
        "console_scripts": [
            "qomma = qomma.__main__:main"
        ]
    },
)
