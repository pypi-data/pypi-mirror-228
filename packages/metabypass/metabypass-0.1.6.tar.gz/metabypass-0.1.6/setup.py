from setuptools import setup, find_packages
REQUIREMENTS = open('requirements.txt','r').read().splitlines()
setup(
    name='metabypass',
    version='0.1.6',
    author='MetaBypass',
    author_email='support@metabypass.tech',
    packages=find_packages(),
    install_requires=REQUIREMENTS,  # List your dependencies
)