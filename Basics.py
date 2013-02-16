import rdflib
import os
import urllib
import sys

QUERY_URL = "http://localhost:8080/openrdf-sesame/repositories/pkb"
UPDATE_URL = "http://localhost:8080/openrdf-sesame/repositories/pkb/statements"
INDIRECT_GRAPH_STORE = "http://localhost:8080/openrdf-sesame/repositories/pkb/rdf-graphs/service"

contentTypes = {
    "rdf": "application/rdf+xml",
    "ttl": "text/turtle; charset=utf-8",
}

def fileurl2path(url):
    url = urllib.parse.urlparse(url)
    if not url.scheme == "file":
        raise SemPipeException("source must be a file")
    return urllib.request.url2pathname(url.path)

def absurl(url, base=None):
    base = base if base else os.path.abspath(".")
    base = "file://" + urllib.request.pathname2url(base)
    if base[-1] != "/": base += "/"
    return urllib.parse.urljoin(base, url)

def guessContentType(url):
    return contentTypes[url.rsplit(".", 1)[-1]]

def put_data(data, identifier, contentType):
    """data can be an open file, an iterable (since Python 3.2), a bytes or a string object"""
    import http.client
    parsedURL = urllib.parse.urlparse(UPDATE_URL)
    connType = { "http": http.client.HTTPConnection, "https": http.client.HTTPSConnection }[parsedURL.scheme]
    connection = connType(parsedURL.hostname, port=parsedURL.port)
    url = "{}?graph={}".format(INDIRECT_GRAPH_STORE, urllib.parse.quote_plus(identifier))
    connection.request("PUT", url, body=data, headers={ 'Content-type': contentType })
    response = connection.getresponse()
    headers = response.getheaders()
    status = response.status
    if not (200 <= status < 300):
        print("PUT failed with status {}:".format(status), file=sys.stderr)
        print("\n".join(["{}: {}".format(*h) for h in headers]), file=sys.stderr)
        print("", file=sys.stderr)
        print(response.read().decode("UTF-8"), file=sys.stderr)
    connection.close()
    return status

def kbConnect():
    kb = rdflib.ConjunctiveGraph("SPARQLUpdateStore", identifier='__UNION__')
    kb.open(("http://localhost:8080/openrdf-sesame/repositories/pkb", "http://localhost:8080/openrdf-sesame/repositories/pkb/statements"))
    return kb
