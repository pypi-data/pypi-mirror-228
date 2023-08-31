import setuptools
from setuptools import setup,  find_packages

setup(
    name="pysideapi",
    version="0.0.2",
    license = "MIT",
    description= "Paquete que me permite trabajar con jira, dicccionario y dictamen",
    author="Jhon Castro",
    author_email= "jhoncc20@gmail.com",
    install_requires=['requests','pytz'],
    packages=find_packages(include=["jira"])

)