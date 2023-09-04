from setuptools import setup, find_packages

setup(
    name='geodesk',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        # Any dependencies your module has, e.g.,
        # 'requests',
    ],
    author='Martin Desmond',
    author_email='martindesmond@gmail.com',
    description='Python port of GeoDesk, a fast and space-efficient statial database engine for OpenStreetMap features',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/clarisma/geodesk',
)
