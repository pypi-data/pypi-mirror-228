from setuptools import setup, find_packages

setup(
    name='znu-nlp',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
          'httpx==0.18.2', # List your dependencies here
    ],
)
