from s2m.core.formulae import *
from s2m.core.variable import *

class Number(Formula):

    def __init__(self, n):

        if type(n) == float \
           or type(n) == int \
           or type(n) == str:
            self.__n = n
        else:
            raise TypeError('Number must be a float, an int or a string, not %r' % n)
        
    def __getattr__(self, p):

        if p == 'n':
            return self.__n
        elif p == 'priority':
            return 5
        elif p == 'val':
            if type(self.__n) == str:
                np = NumberParser()
                return np(self.__n)
            else:
                return self.__n
        else:
            raise AttributeError

    def count_brackets(self):

        return 0, 0

    def distance(self, f):
        numbers = 0.1
        variables = 0.5
        others = 1.
        if f.__class__ == Number:
            if f.val == self.val:
                return 0.
            else:
                return numbers
        elif f.__class__ == Variable:
            return variables
        elif issubclass(f.__class__, Formula):
            return others
        else:
            raise TypeError('Cannot compare Number to non-formula %r' % f)

    def symmetry_index(self):

        return 1.

    def _latex(self):

        return repr(self.val), 0
        
    def latex(self):

        return repr(self.val)

    def concat(self, p):

        if type(self.__n) == str \
           and p.__class__ == Number \
           and type(p.n) == str:
            return Number(self.__n + " " + p.n)
        else:
            raise TypeError('Concatenation of Numbers must be applied to Number classes ' \
                            + 'with string-encoded attributes.')

    def teach(parser):

        def number_reduce(word):
            if word in NumberParser.NUMBER_WORDS:
                return Token('number', [Number(word)])
            else:
                return None

        def number_expand(tok1, tok2):
            if tok1.tag == tok2.tag == 'number':
                return Token('number', [tok1.formula[0].concat(tok2.formula[0])])
            else:
                return None

        parser.add_reduce(number_reduce)
        parser.add_expand(number_expand)

