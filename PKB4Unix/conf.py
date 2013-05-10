from sys import argv
import os
import textwrap
from rdflib import Namespace, URIRef

class ConfVarInfo():
    __slots__ = ('name', 'shortopt', 'metavar', 'help', 'translate_func',
                 'default', 'fromcmdline', 'fromenv',
                 'value', 'blame')

    def __init__(self, *initial_list, **initial):
        for (k,v) in zip(ConfVarInfo.__slots__, initial_list):
            setattr(self, k, v)
        for k in initial.keys():
            setattr(self, k, initial[k])
        self._compute_value()

    @property
    def longopt(self):
        return self.name.lower().replace('_','-')

    @property
    def envvar(self):
        return self.fromenv and 'KNOW_'+self.name or None

    @property
    def cmdline_short(self):
        return self.fromcmdline and '-'+self.shortopt or None

    @property
    def cmdline_long(self):
        return self.fromcmdline and '--'+self.longopt or None

    def set(self, value, blame='internal change'):
        self.value = value
        self.blame = blame

    def commit(self):
        globals()[self.name] = self.translate_func(self.value)

    def setenv(self):
        if self.fromenv:
            os.environ[self.envvar] = self.value

    def _compute_value(self):
        if self.fromenv and self.envvar in os.environ:
            self.value = os.environ[self.envvar]
            self.blame = 'environment'
        else:
            self.value = self.default
            self.blame = 'default'

confvars = [
    ConfVarInfo(
        'ENDPOINT_QUERY',
        'Q',
        'URL',
        "URL of the SPARQL endpoint for queries",
        lambda value: value,
        "http://localhost:8080/openrdf-sesame/repositories/pkb", 
        True,
        True,
    ),
    ConfVarInfo(
        'ENDPOINT_UPDATE',
        'U',
        'URL',
        "URL of the SPARQL endpoint for updates",
        lambda value: value,
        "http://localhost:8080/openrdf-sesame/repositories/pkb/statements",
        True,
        True,
    ),
    ConfVarInfo(
        'ENDPOINT_INDIRECT',
        'I',
        'URL',
        "URL of the SPARQL endpoint's inditirect graph store",
        lambda value: value,
        "http://localhost:8080/openrdf-sesame/repositories/pkb/rdf-graphs/service",
        True,
        True,
    ),
    ConfVarInfo(
        'PROVENANCE_GRAPH',
        'P',
        'URI',
        "URI of the graph storing provenance information",
        lambda value: URIRef(value),
        "kb:provenance",
        True,
        True,
    ),
    ConfVarInfo(
        'NS_GRAPH',
        'N',
        'URI',
        "URI of the graph containing information about namespaces",
        lambda value: Namespace(value),
        "kb:namespaces",
        True,
        True,
    ),
    ConfVarInfo(
        'NS_KB',
        None,
        'URI',
        "The namespace of the PKB configuration vocabulary",
        lambda value: Namespace(value),
        "http://www.andonyar.com/rec/2012/pkb/conf#",
        False,
        False,
    ),
]

for var in confvars:
    var.commit()    

__all__ = [var.name for var in confvars]

