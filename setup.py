from setuptools import setup
import os

VERSION = "0.1.0"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-matomo",
    description="Add Matomo Web Analytics tracking code to Datasette",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="UUDigitalHumanitiesLab",
    author_email="digitalhumanities@uu.nl",
    url="https://github.com/UUDigitalHumanitieslab/datasette-matomo",
    project_urls={
        "Issues": "https://github.com/UUDigitalHumanitieslab/datasette-matomo/issues",
        "CI": "https://github.com/UUDigitalHumanitieslab/datasette-matomo/actions",
        "Changelog": "https://github.com/UUDigitalHumanitieslab/datasette-matomo/releases",
    },
    license="Apache License, Version 2.0",
    classifiers=[
        "Framework :: Datasette",
        "License :: OSI Approved :: Apache Software License"
    ],
    version=VERSION,
    packages=["datasette_matomo"],
    entry_points={"datasette": ["matomo = datasette_matomo"]},
    install_requires=["datasette"],
    extras_require={"test": ["pytest", "pytest-asyncio"]},
    package_data={
        "datasette_matomo": ["templates/*"]
    },
    python_requires=">=3.7",
)
