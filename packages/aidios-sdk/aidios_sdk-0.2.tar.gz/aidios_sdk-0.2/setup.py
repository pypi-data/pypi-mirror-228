from setuptools import setup, find_packages

setup(
    name='aidios_sdk',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    author='Jamie Gilchrist',
    author_email='jamie.gilchrist@tunestamp.com',
    description='SDK for the Aidios API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://aidios.co.uk',
)

