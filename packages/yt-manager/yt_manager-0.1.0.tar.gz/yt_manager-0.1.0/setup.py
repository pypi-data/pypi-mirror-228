from setuptools import setup, find_packages

setup(
    name='yt_manager',
    version='0.1.0',
    url='https://github.com/CBoYXD/yt_manager',
    license='MIT',
    author='CBoYXD',
    author_email='python.rust.cpp@gmail.com',
    description='Youtube manager based on Selenium',
    packages=find_packages(exclude=['tests']),
    long_description=open('README.md').read()
)