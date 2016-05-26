"""Distutils file for metagenomix."""
from setuptools import setup, find_packages


requires = ['BioPython']

setup(
    name = 'metagenomix',
    description = 'Metagenomic analysis pipeline',
    url = 'github/pgnd-meta',
    author = 'Ana Bulovic',
    author_email = 'bulovic.ana@gmail.com',
    license = 'MIT',
    long_description = open('README.md').read(),
    packages = find_packages(),
    scripts = [],
    package_data = {'meta.data': ['taxid2namerank', 'ncbi_tax_tree', 'NCBI.db']},
    data_files = [('', ['README.md'])],
    entry_points = {
        'console_scripts': [
            'ncbi-download = meta.data.NCBI:__download__',
            'fq2fa = meta.io.seq:fq2fa'
        ]
    },
    install_requires=requires,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: Freeware',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
        ],
    )