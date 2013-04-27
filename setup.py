#!/usr/bin/env python

from distutils.core import setup

setup(name='pkb4unix',
      version='0.1',
      description='A personal knowledge base using RDF and SPARQL following the UNIX philosophy',
      author='Urs Holzer',
      author_email='urs@andonyar.com',
      url='http://www.andonyar.com/rec/2012/pkb/',
      py_modules=['PKB4Unix'],
      scripts=[
        'know',
        'know-graph',
        'know-load',
        'know-merge',
        'know-query',
        'know-query-template',
        'know-rdf-construct',
        'know-rdf-edit',
        'know-rdf-format-csv',
        'know-rdf-uuid',
        'know-rm',
        'know-save',
        'know-search',
      ],
      keywords=['Requires: rdflib'],
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
            "Operating System :: POSIX",
            "Natural Language :: English",
      ]
     )

