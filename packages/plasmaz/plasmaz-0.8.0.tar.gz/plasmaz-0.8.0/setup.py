from setuptools import setup, find_packages

setup(
    name='plasmaz',
    version='0.8.0',
    description='Plasmaz is a Python GitHub API wrapper which interacts with the GitHub API.',
    packages=find_packages(),
    license='MIT License (MIT)',
    author='TuberAsk',
    install_requires=['requests'],
)
