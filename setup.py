from setuptools import setup, find_packages
from os import path
import sys

if not sys.version_info >= (3,4):
    print("Error: pkb4unix requires at least Python 3.4.")
    exit(1)

setup(
    name='PKB4Unix',
    version='0.1.0',
    description='A personal knowledge base using RDF and SPARQL following the UNIX philosophy',
    author='Urs Holzer',
    author_email='urs@andonyar.com',
    url='http://www.andonyar.com/rec/2012/pkb/',
    license='GPLv3+',
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
    ],
    keywords='semantic web knowledge base',
    packages=['PKB4Unix'],
    install_requires=[
        'rdflib>=4.2.0',
    ],
    package_data={
        'pkb4unix.calendar': ['ontology/*.trig'],
    },
    data_files=[
        ('share/pkb4unix/templates', [
            'templates/README',
            'templates/task.tmpl',
            'templates/website.tmpl',
        ]),
    ],
    scripts = [
        'know',
        'know-construct',
        'know-convert',
        'know-edit',
        'know-format-csv',
        'know-merge',
        'know-search',
        'know-sparql-construct',
        'know-sparql-discover',
        'know-sparql-graph',
        'know-sparql-load',
        'know-sparql-merge',
        'know-sparql-query',
        'know-sparql-query-template',
        'know-sparql-render',
        'know-sparql-rm',
        'know-sparql-save',
    ],
)
