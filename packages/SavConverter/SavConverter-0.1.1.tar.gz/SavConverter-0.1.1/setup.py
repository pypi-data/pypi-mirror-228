from setuptools import setup, find_packages

setup(
    name='SavConverter',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[],
    author='Ryan Grissett',
    author_email='ryan.grissett@hotmail.com',
    description="Python-GVAS-JSON-Converter (SavConverter) is a library designed to convert Unreal Engine's Game Variable and Attribute System (GVAS) files between .sav and .json formats.",
    url='https://github.com/afkaf/Python-GVAS-JSON-Converter',
    license='Unlicense',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3'
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
