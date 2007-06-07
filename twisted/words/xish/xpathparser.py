# Copyright (c) 2001-2007 Twisted Matrix Laboratories.
# See LICENSE for details.

# DO NOT EDIT xpathparser.py!
#
# It is generated from xpathparser.g using Yapps. Make needed changes there.
# This also means that the generated Python may not conform to Twisted's coding
# standards.

# HOWTO Generate me:
# 1.) Grab a copy of yapps2: http://theory.stanford.edu/~amitp/Yapps/
#     (available on debian by "apt-get install -t unstable yapps2")
# 2.) Generate the grammar as usual
# 3.) Hack the output to read:
#
#         import twisted.words.xish.yappsrt as runtime
#
#       instead of
#
#         from yapps import runtime

from twisted.words.xish.xpath import AttribValue, BooleanValue, CompareValue
from twisted.words.xish.xpath import Function, IndexValue, LiteralValue
from twisted.words.xish.xpath import _AnyLocation, _Location


# Begin -- grammar generated by Yapps
import sys, re
import twisted.words.xish.yappsrt as runtime

class XPathParserScanner(runtime.Scanner):
    patterns = [
        ('","', re.compile(',')),
        ('"@"', re.compile('@')),
        ('"\\)"', re.compile('\\)')),
        ('"\\("', re.compile('\\(')),
        ('"\\]"', re.compile('\\]')),
        ('"\\["', re.compile('\\[')),
        ('"//"', re.compile('//')),
        ('"/"', re.compile('/')),
        ('\\s+', re.compile('\\s+')),
        ('INDEX', re.compile('[0-9]+')),
        ('WILDCARD', re.compile('\\*')),
        ('IDENTIFIER', re.compile('[a-zA-Z][a-zA-Z0-9_\\-]*')),
        ('ATTRIBUTE', re.compile('\\@[a-zA-Z][a-zA-Z0-9_\\-]*')),
        ('FUNCNAME', re.compile('[a-zA-Z][a-zA-Z0-9_]*')),
        ('CMP_EQ', re.compile('\\=')),
        ('CMP_NE', re.compile('\\!\\=')),
        ('STR_DQ', re.compile('"([^"]|(\\"))*?"')),
        ('STR_SQ', re.compile("'([^']|(\\'))*?'")),
        ('OP_AND', re.compile('and')),
        ('OP_OR', re.compile('or')),
        ('END', re.compile('$')),
    ]
    def __init__(self, str,*args,**kw):
        runtime.Scanner.__init__(self,None,{'\\s+':None,},str,*args,**kw)

class XPathParser(runtime.Parser):
    Context = runtime.Context
    def XPATH(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'XPATH', [])
        PATH = self.PATH(_context)
        result = PATH; current = result
        while self._peek('END', '"/"', '"//"', context=_context) != 'END':
            PATH = self.PATH(_context)
            current.childLocation = PATH; current = current.childLocation
        END = self._scan('END', context=_context)
        return  result

    def PATH(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'PATH', [])
        _token = self._peek('"/"', '"//"', context=_context)
        if _token == '"/"':
            self._scan('"/"', context=_context)
            result = _Location()
        else: # == '"//"'
            self._scan('"//"', context=_context)
            result = _AnyLocation()
        _token = self._peek('IDENTIFIER', 'WILDCARD', context=_context)
        if _token == 'IDENTIFIER':
            IDENTIFIER = self._scan('IDENTIFIER', context=_context)
            result.elementName = IDENTIFIER
        else: # == 'WILDCARD'
            WILDCARD = self._scan('WILDCARD', context=_context)
            result.elementName = None
        while self._peek('"\\["', 'END', '"/"', '"//"', context=_context) == '"\\["':
            self._scan('"\\["', context=_context)
            PREDICATE = self.PREDICATE(_context)
            result.predicates.append(PREDICATE)
            self._scan('"\\]"', context=_context)
        return result

    def PREDICATE(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'PREDICATE', [])
        _token = self._peek('INDEX', '"\\("', '"@"', 'FUNCNAME', 'STR_DQ', 'STR_SQ', context=_context)
        if _token != 'INDEX':
            EXPR = self.EXPR(_context)
            return EXPR
        else: # == 'INDEX'
            INDEX = self._scan('INDEX', context=_context)
            return IndexValue(INDEX)

    def EXPR(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'EXPR', [])
        FACTOR = self.FACTOR(_context)
        e = FACTOR
        while self._peek('OP_AND', 'OP_OR', '"\\)"', '"\\]"', context=_context) in ['OP_AND', 'OP_OR']:
            BOOLOP = self.BOOLOP(_context)
            FACTOR = self.FACTOR(_context)
            e = BooleanValue(e, BOOLOP, FACTOR)
        return e

    def BOOLOP(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'BOOLOP', [])
        _token = self._peek('OP_AND', 'OP_OR', context=_context)
        if _token == 'OP_AND':
            OP_AND = self._scan('OP_AND', context=_context)
            return OP_AND
        else: # == 'OP_OR'
            OP_OR = self._scan('OP_OR', context=_context)
            return OP_OR

    def FACTOR(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'FACTOR', [])
        _token = self._peek('"\\("', '"@"', 'FUNCNAME', 'STR_DQ', 'STR_SQ', context=_context)
        if _token != '"\\("':
            TERM = self.TERM(_context)
            return TERM
        else: # == '"\\("'
            self._scan('"\\("', context=_context)
            EXPR = self.EXPR(_context)
            self._scan('"\\)"', context=_context)
            return EXPR

    def TERM(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'TERM', [])
        VALUE = self.VALUE(_context)
        t = VALUE
        if self._peek('CMP_EQ', 'CMP_NE', 'OP_AND', 'OP_OR', '"\\)"', '"\\]"', context=_context) in ['CMP_EQ', 'CMP_NE']:
            CMP = self.CMP(_context)
            VALUE = self.VALUE(_context)
            t = CompareValue(t, CMP, VALUE)
        return t

    def VALUE(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'VALUE', [])
        _token = self._peek('"@"', 'FUNCNAME', 'STR_DQ', 'STR_SQ', context=_context)
        if _token == '"@"':
            self._scan('"@"', context=_context)
            IDENTIFIER = self._scan('IDENTIFIER', context=_context)
            return AttribValue(IDENTIFIER)
        elif _token == 'FUNCNAME':
            FUNCNAME = self._scan('FUNCNAME', context=_context)
            f = Function(FUNCNAME); args = []
            self._scan('"\\("', context=_context)
            if self._peek('"\\)"', '"@"', 'FUNCNAME', '","', 'STR_DQ', 'STR_SQ', context=_context) not in ['"\\)"', '","']:
                VALUE = self.VALUE(_context)
                args.append(VALUE)
                while self._peek('","', '"\\)"', context=_context) == '","':
                    self._scan('","', context=_context)
                    VALUE = self.VALUE(_context)
                    args.append(VALUE)
            self._scan('"\\)"', context=_context)
            f.setParams(*args); return f
        else: # in ['STR_DQ', 'STR_SQ']
            STR = self.STR(_context)
            return LiteralValue(STR[1:len(STR)-1])

    def CMP(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'CMP', [])
        _token = self._peek('CMP_EQ', 'CMP_NE', context=_context)
        if _token == 'CMP_EQ':
            CMP_EQ = self._scan('CMP_EQ', context=_context)
            return CMP_EQ
        else: # == 'CMP_NE'
            CMP_NE = self._scan('CMP_NE', context=_context)
            return CMP_NE

    def STR(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'STR', [])
        _token = self._peek('STR_DQ', 'STR_SQ', context=_context)
        if _token == 'STR_DQ':
            STR_DQ = self._scan('STR_DQ', context=_context)
            return STR_DQ
        else: # == 'STR_SQ'
            STR_SQ = self._scan('STR_SQ', context=_context)
            return STR_SQ


def parse(rule, text):
    P = XPathParser(XPathParserScanner(text))
    return runtime.wrap_error_reporter(P, rule)

if __name__ == '__main__':
    from sys import argv, stdin
    if len(argv) >= 2:
        if len(argv) >= 3:
            f = open(argv[2],'r')
        else:
            f = stdin
        print parse(argv[1], f.read())
    else: print >>sys.stderr, 'Args:  <rule> [<filename>]'
# End -- grammar generated by Yapps
