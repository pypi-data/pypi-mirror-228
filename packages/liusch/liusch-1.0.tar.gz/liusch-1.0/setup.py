from setuptools import setup

setup(
    name="liusch",
    version="1.0",
    packages=["liusch"],
    entry_points={
        "console_scripts": [
            "liusch = liusch.main:main"
        ]
    },
)

