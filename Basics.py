import rdflib

def kbConnect():
    kb = rdflib.ConjunctiveGraph("SPARQLUpdateStore", identifier='__UNION__')
    kb.open(("http://localhost:8080/openrdf-sesame/repositories/pkb", "http://localhost:8080/openrdf-sesame/repositories/pkb/statements"))
    return kb
