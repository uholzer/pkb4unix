import re
import itertools
from collections import defaultdict, namedtuple
import subprocess
from rdflib import Graph, Literal, BNode, URIRef

COUNT_ONEORNONE = -1
COUNT_ONEORMORE = -2
COUNT_ANY = -3

class TemplateError(Exception):
    pass

class NotPName(Exception):
    pass

class PrefixNotFound(Exception):
    pass

TemplateVariable = namedtuple('TemplateVariable', [
    'nodetype',
    'count',
    'name',
    'classhint',
    'datatypehint',
    'langhint',
    'prompt'
    ])

class Section:
    def __init__(self):
        self.name = ""
        self.quads = ""
        self.mainvariable = None
        self.variables = list()
        self.ns = dict()
        self.expand_re = re.compile(r"^([^\s]*):([^\s]*)$")

    def expand(self, shortname):
        match = self.expand_re.match(shortname)
        if match:
            prefix = match.group(1)
            localname = match.group(2)
            try:
                return self.ns[prefix] + localname
            except KeyError:
                raise PrefixNotFound()
        else:
            raise NotPName()

    def construct(self, g, sections, mainvar_value=None):
        raise NotImplementedError()

class TerminalSection(Section):
    def __init__(self, out):
        super().__init__()
        self.out = out

    def construct(self, g, sections, mainvar_value=None):
        print("", file=self.out)
        print("=== {}".format(self.name), file=self.out)
        varvalues = defaultdict(list)

        print("I will insert the following triples:\n"+self.quads, file=self.out)

        if not mainvar_value:
            mainvar_value = self.input("CONSTRUCTING {}> ".format(self.mainvariable.prompt))
            mainvar_value = URIRef(mainvar_value)
            varvalues[self.mainvariable.name].append(mainvar_value)
        else:
            varvalues[self.mainvariable.name].append(mainvar_value)
            
        for var in self.variables:
            askfunc = getattr(self, "ask_" + var.nodetype)

            if var.count > 0:
                r = range(0, var.count)
            elif var.count == COUNT_ONEORNONE:
                r = range(0, 1)
            elif var.count == COUNT_ANY or var.count == COUNT_ONEORMORE:
                r = itertools.count(0)
            else:
                raise Error("Invalide count")
                
            for i in r:
                val = askfunc(g, sections, var, self.prompt(var.nodetype, i, var.count, var.prompt))
                if not str(val): # val itself could be false: "false"^^xsd:bool
                    break
                varvalues[var.name].append(val)

        where_part = ""
        for (var, values) in varvalues.items():
            values_list = " ".join("({})".format(v.n3()) for v in values)
            where_part += "VALUES ({}) {{ {} }}\n".format(str(var), values_list)
        q = "INSERT {{\n{}}}\nWHERE {{\n{}}}".format(self.quads, where_part)

        print("Adding tribles with SPARQL:\n"+q, file=self.out)

        g.update(q, initNs=self.ns)

        print("=== {}".format("done"), file=self.out)
        print("", file=self.out)

        return mainvar_value

    def ask_NODE(self, g, sections, var):
        raise NotImplemented()

    def ask_RESOURCE(self, g, sections, var, prompt):
        if var.classhint and var.classhint in sections:
            answer = self.input(prompt)
            if answer == "c":
                s = sections[var.classhint]
                node = s.construct(g, sections, None)
                print("back to {}".format(self.name), file=self.out)
                return node
            else:
                return URIRef(answer)
        else:
            answer = self.input(prompt)
            return URIRef(answer)

    def ask_LITERAL(self, g, sections, var, prompt):
        answer = self.input(prompt)
        # TODO: Let the user set datatype or language.
        
        return Literal(answer, lang=var.langhint, datatype=var.datatypehint)

    def ask_BNODE(self, g, sections, var, prompt):
        # In order to implement casshints and construction,
        # one would create a blank node and then call
        # section.construct(g, sections, theNewBNode)
        print("{} ({}):".format(varname, descr), file=self.out)
        answer = self.input(prompt)
        return BNode()

    def prompt(self, nodetype, number, count, text):
        if count == COUNT_ANY:
            count = "*"
        if count == COUNT_ONEORNONE:
            count = "?"
        elif count == COUNT_ONEORMORE:
            count = "+"
        return "{}{}/{} {}> ".format(nodetype, number+1, count, text)

    def input(self, prompt):
        value = input(prompt)
        if value:
            if value[0] == '@':
                value = '| ./know-rdf-edit --null'
            if value[0] == '!':
                subprocess.call(value[1:], shell=True, stdout=self.out)
                return self.input(prompt) # start over
            elif value[0] == '|':
                try:
                    value = subprocess.check_output(value[1:], shell=True, universal_newlines=True)
                    # universal_newlines=True causes value to be a string
                except subprocess.CalledProcessError:
                    print("Your shell command failed, try again!", file=self.out)
                    return self.input(prompt)
        if value and value[-1] == '\n':
            # Remove last newline in order to simplify
            # providing single-line literals and URIs.
            value = value[0:-1]
        return value

class Parser:
    def __init__(self, sectionFactory=Section):
        self.sectionFactory = sectionFactory
        self.classhint_re = re.compile(r"^\[([^\]]*)\]")
        self.globalns = dict()
        self.sections = dict()

    def parse(self, lineiter):
        current_section = None
        first_section = None
        # Preamble
        while True:
            try:
                line = next(lineiter)
            except StopIteration:
                raise TemplateError("Tempalte contains no section")
            line = line.strip()
            if line=="" or line[0] == '#':
                pass
            elif line[0] == '[':
                current_section = self.startSection(line)
                first_section = current_section
                break
            elif line.split(None, 1)[0] == 'NS':
                self.really_parse_NS(self.globalns, line)
            else:
                raise TemplateError("Only NS declarations allowed in the preamble")
        # Sections
        while True:
            try:
                line = next(lineiter)
            except StopIteration:
                break
            line = line.strip()
            if line=="" or line[0] == '#':
                pass
            elif line[0] == '[':
                current_section = self.startSection(line)
            else:
                instruction = line.split(None, 1)[0]
                try:
                    pfunc = getattr(self, "parse_" + instruction)
                except AttributeError:
                    raise TemplateError("Unknown instruction '{}'".format(instruction))
                pfunc(current_section, line, lineiter)
            
        return (self.sections, first_section)

    def really_parse_NS(self, ns, argline):
        args = argline.split(None, 2)
        if not args[1][-1] == ':':
            raise TemplateError("Prefix must end in :")
        ns[args[1][0:-1]] = args[2]

    def parse_NS(self, section, argline, lineiter):
        self.really_parse_NS(section.ns, argline)
        
    def parse_NODE(self, section, argline, lineiter):
        args = argline.split(None, 3)
        classhint = None
        datatypehint = None
        langhint = None
        if args[0] == "LITERAL":
            (datatypehint, langhint) = self.lithint(section, args[3])
        else:
            classhint = self.classhint(section, args[3])
        var = TemplateVariable(
            nodetype=args[0],
            count=self.count(args[1]),
            name=self.variable(args[2]),
            classhint=classhint,
            datatypehint=datatypehint,
            langhint=langhint,
            prompt=args[3]
        )
        section.variables.append(var)

    parse_RESOURCE = parse_NODE
    parse_LITERAL = parse_NODE
    parse_BNODE = parse_NODE

    def parse_INSERT(self, section, argline, lineiter):
        if not argline.split(None, 1) == ["INSERT", "{"]:
            raise
        quads = ""
        try:
            line = next(lineiter)
            while line.rstrip() != '}': # } must be at beginning of line
                quads += line
                line = next(lineiter)
        except StopIteration:
            raise TemplateError("INSERT block not closed at EOF")
        section.quads = quads

    def startSection(self, line):
        section = self.sectionFactory()
        section.ns = dict(self.globalns) # Include globally defined namespaces
        args = line.split(None, 2)
        c = self.classhint(section, args[0])
        if not c:
            raise TemplateError("Invalid Syntax in section start")
        section.name = c
        self.sections[c] = section

        section.mainvariable = TemplateVariable(
            nodetype="RESOURCE",
            count=1,
            name=self.variable(args[1]),
            classhint=c,
            datatypehint=None,
            langhint=None,
            prompt=args[2]
        )
        return section

    def count(self, s):
        if s == '*':
            return COUNT_ANY
        elif s == '+':
            return COUNT_ONEORMORE
        elif s == '?':
            return COUNT_ONEORNONE
        else:
            try:
                return int(s)
            except:
                raise TemplateError("Count expected")

    def variable(self, s):
        if s[0] == '?' or s[0] == '$':
            return s
        else:
            raise TemplateError("Variable expected")

    def classhint(self, section, s):
        match = self.classhint_re.search(s)
        if match:
            hint = match.group(1)
            try:
                return section.expand(hint)
            except NotPName:
                return hint
        else:
            return None

    def lithint(self, section, s):
        match = self.classhint_re.search(s)
        if match:
            hint = match.group(1)
            if hint.startswith("^^"):
                return (URIRef(section.expand(hint[2:])), None)
            elif hint.startswith("@"):
                return (None, hint[1:])
            else:
                raise TemplateError("Malformed literal type hint")
        else:
            return (None, None)

