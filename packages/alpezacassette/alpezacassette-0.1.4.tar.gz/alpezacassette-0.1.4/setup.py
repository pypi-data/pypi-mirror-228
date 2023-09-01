from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()


def getRequirements():
    with open("requirements.txt", "r", encoding="utf-8") as requirements_file:
        install_requires = [line.strip()
                            for line in requirements_file if line.strip()]


setup(
    name="alpezacassette",
    version="0.1.4",
    description="Renderizador de dialogos .fountain a audio",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="alpeza",
    packages=find_packages(),
    include_package_data=True,
    install_requires=getRequirements(),
    url="https://github.com/alpeza/cassette",
    entry_points={
        "console_scripts": [
            "cassette = cassette.main:main",
        ],
    },
    package_data={
        "": ["utils/.env"],
    },
)
