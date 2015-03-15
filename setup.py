from setuptools import setup, find_packages
from os import path
import sys

if not sys.version_info >= (3,4):
    print("Error: pkb4unix requires at least Python 3.4.")
    exit(1)


here = path.abspath(path.dirname(__file__))

# Extract the description from the README
with open(path.join(here, 'README'), encoding='utf-8') as f:
    title = f.readline().strip()
    oneline_description = f.readline().strip()
    assert len(oneline_description) <= 60, 'Description on line 2 of README too long'
    assert f.readline().strip() == '', 'README has bad format for extraction of description'
    long_description = ''
    for l in iter(f.readline, ''):
        if l.strip() == '':
            break
        long_description += l

setup(
    name='pkb4unix',
    # Version number conforming to
    # http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers
    version='0.1.1.dev0',
    description=oneline_description,
    long_description=long_description,
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
