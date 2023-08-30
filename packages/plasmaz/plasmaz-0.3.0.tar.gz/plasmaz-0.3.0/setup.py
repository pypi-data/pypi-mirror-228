from setuptools import setup, find_packages

setup(
    name='plasmaz',
    version='0.3.0',
    description='Plasmaz is a Python GitHub API wrapper which interacts with the GitHub API and creates a smoother experience for developing with GitHub in Python.',
    packages=find_packages(),
    license='MIT',
    author='TuberAsk',
    install_requires=['Python>=3.8', 'requests'],
)
