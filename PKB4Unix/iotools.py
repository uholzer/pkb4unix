"""Tools to handle URIs, contentTypes, read files, and do http requests
"""

import os
import mimetypes
import urllib
from .conf import *

# Adding some uncommon mime-types
mimetypes.init()
mimetypes.add_type("application/rdf+xml", ".rdf")
mimetypes.add_type("application/n-triples", ".nt")
mimetypes.add_type("text/turtle", ".ttl")
mimetypes.add_type("text/n3", ".n3")
mimetypes.add_type("application/n-quads", ".nq")

defaultAcceptHeader = DEFAULT_FORMAT + "; q=1";
for f in ["text/turtle", "application/rdf+xml", "application/n-triples", "text/n3"]:
    if f != DEFAULT_FORMAT:
        defaultAcceptHeader += ", {}; q=0.99".format(f)

def guess_contentType(url, include_charset=False):
    (t, enc) = mimetypes.guess_type(url)
    if include_charset and t.startswith("text/"):
        return "{}; charset={}".format(t, "utf-8")
    else:
        return t

def url2localpath(url):
    """Converts a URL into the local syntax of a path

    Throws a ValueError if the URL is not a file URL."""
    url = urllib.parse.urlparse(url, scheme='file') # scheme='file' in case of realtive URL
    if not url.scheme == "file":
        raise ValueError("Not a file URL")
    return urllib.request.url2pathname(url.path)

def absurl(url, base=None):
    """Makes an absolute URL from a relative one

    In order to make it possible to also use filenames as url, it gets
    quoted first. Only characters not allowed in URLs are quoted. This
    means that certain filenames (those with : or % in their name)
    will not be treated the right way. The reason for this behaviour
    is that an URI like urn:uuid:something could really be a filename
    but is also an absolute URI and has to be interpreted as such."""
    base = base if base else os.path.abspath(".")
    base = "file://" + urllib.request.pathname2url(base)
    url = urllib.parse.quote_plus(url, safe=":/?#[]@!$&'()*+,;=-._~%")
    if base[-1] != "/": base += "/"
    return urllib.parse.urljoin(base, url)
