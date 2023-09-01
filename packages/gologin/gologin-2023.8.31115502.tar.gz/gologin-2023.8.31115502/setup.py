from setuptools import setup, find_packages

setup(
    name='gologin',
    version='2023.08.31115502',
    packages=find_packages(),
    install_requires=[
        # Deps
    ],
    author='GoLogin',
    author_email='yuri@gologin.com',
    description='Official GoLogin python package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/gologinapp/pygologin',
    python_requires='>=3.5'
)
