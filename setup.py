from setuptools import setup, find_packages

setup(
    name='bookbnb_middleware',
    version='1.0.0',
    description='Middleware for integrating BookBNB microservices',
    url='https://github.com/7552-2020C2-grupo5/middleware',
    author='Leonardo Bellaera',

    packages=find_packages(),

    install_requires=['flask-restx'],
)
