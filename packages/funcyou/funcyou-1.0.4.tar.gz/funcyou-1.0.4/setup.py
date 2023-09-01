
from setuptools import setup, find_packages

setup(
    name='funcyou',
    version='1.0.4',
    author='Tikendra sahu',
    author_email='tikendraksahu1029@gmail.com',
    description='useful function to save time',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'sklearn',
        'pandas',
        'numpy',
        'kaggle'
        # Add other dependencies here
    ],
)
