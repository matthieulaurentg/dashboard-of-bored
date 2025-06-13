#!/usr/bin/env python3
"""
Setup script for Three Card Roulette
Creates an installable package with auto-update capabilities
"""
from setuptools import setup, find_packages
import os

# Read version from version file
def get_version():
    version_file = os.path.join(os.path.dirname(__file__), 'version.txt')
    if os.path.exists(version_file):
        with open(version_file, 'r') as f:
            return f.read().strip()
    return '1.0.0'

# Read README for long description
def get_long_description():
    readme_file = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_file):
        with open(readme_file, 'r', encoding='utf-8') as f:
            return f.read()
    return 'Three Card Roulette - Casino game with stock trading'

setup(
    name='three-card-roulette',
    version=get_version(),
    author='Matthieu',
    author_email='matthieu@example.com',
    description='A casino card game with real-time stock trading and achievements',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/matthieu/three-card-roulette',
    packages=find_packages(),
    py_modules=[
        'game',
        'languages', 
        'stock_market',
        'achievements',
        'card_game',
        'updater'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Games/Entertainment',
        'Topic :: Games/Entertainment :: Arcade',
    ],
    python_requires='>=3.7',
    install_requires=[
        'requests>=2.25.0',
    ],
    entry_points={
        'console_scripts': [
            'three-card-roulette=game:main',
            'tcr=game:main',
        ],
    },
    include_package_data=True,
    package_data={
        '': ['*.txt', '*.md', '*.json'],
    },
    zip_safe=False,
)