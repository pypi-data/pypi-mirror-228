from setuptools import setup, find_packages

setup(
    name='zjsar',
    version='1.0.0',
    description='zJSAR - New compressions',
    author='Nelyon',
    author_email='pauline.darrieux@gmail.com',
    packages=find_packages(),
    install_requires=["cryptography"],
)
