#!/usr/bin/env python

import sys
from distutils.core import setup

if not sys.version_info >= (3,2):
    print("Error: pkb4unix requires at least Python 3.2.")
    exit(1)

setup(name='pkb4unix',
      version='0.1',
      description='A personal knowledge base using RDF and SPARQL following the UNIX philosophy',
      author='Urs Holzer',
      author_email='urs@andonyar.com',
      url='http://www.andonyar.com/rec/2012/pkb/',
      packages=['PKB4Unix'],
      scripts=[
        'know',
        'know-construct',
        'know-graph',
        'know-load',
        'know-merge',
        'know-query',
        'know-query-template',
        'know-rdf-construct',
        'know-rdf-edit',
        'know-rdf-format-csv',
        'know-rdf-uuid',
        'know-render',
        'know-rm',
        'know-save',
        'know-search',
      ],
      keywords=['Requires: rdflib'],
      data_files=[
            ('share/pkb4unix/templates', [
                'templates/README',
                'templates/task.tmpl',
                'templates/website.tmpl',
            ])
      ],
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
            "Operating System :: POSIX",
            "Natural Language :: English",
      ]
     )

