import os, sys, re
from setuptools import setup, find_packages

with open(os.path.join('kana_arranger', '__init__.py')) as f:
    version = re.search(r'__version__\s*=\s*["\'](.*?)["\']', f.read()).group(1)

with open(os.path.join('.', 'requirements.txt'), 'r') as f:
    requirements = [line.rstrip() for line in f]

setup(
    name='kana_arranger',
    version=version,
    description='Evaluates various romaji/kana input methods.',
    url='https://github.com/mobitan/kana_arranger',
    author='mobitan',
    author_email='webmaster@mobitan.org',
    license='Apache License 2.0',
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=requirements,
)