from s2m.core.formulae import Formula
from s2m.core.variable import Variable
from s2m.core.number_parser import NumberParser
from s2m.core.parser import Token

import os
import numpy

class Number(Formula):

    def __init__(self, n):

        if type(n) == float \
           or type(n) == int:
            self.__n = n
            self.__val = n
        elif type(n) == str:
            self.__n = n
            np = NumberParser()
            try:
                self.__val = np(n, strict=True)
            except ValueError:
                raise ValueError('String %r cannot be interpreted as a number' % n)
        else:
            raise TypeError('Number must be a float, an int or a string, not %r' % n)

    def __getattr__(self, p):

        if p == 'n':
            return self.__n
        if p == 'val':
            return self.__val     
        elif p == 'priority':
            return 5
        else:
            raise AttributeError

    def __eq__(self, other):
	
        if other and isinstance(other, Number):
            return other.val == self.__val
        return False 

    def __hash__(self):

        return hash(self.__val)

    def count_brackets(self):

        return 0, 0

    def distance(self, f):

        from s2m.core.variable import Variable

        numbers = 0.1
        variables = 0.5
        others = 1.
        if isinstance(f, Number):
            if f.val == self.__val:
                return 0.
            else:
                return numbers
        elif isinstance(f, Variable):
            return variables
        elif isinstance(f, Formula):
            return others
        else:
            raise TypeError('Cannot compare Number to non-formula %r' % f)

    def symmetry_index(self):

        return 1.

    def _latex(self):

        return repr(self.__val), 0

    def latex(self):

        return repr(self.__val)

    def transcription(self):

        np = NumberParser()
        return np.transcribe(self.val)

    @classmethod
    def teach(cls, parser):

        def number_reduce(word):
            if word in NumberParser.NUMBER_WORDS:
                try:
                    return Token('number', [Number(word)])
                except:
                    return Token('number', [word])
            else:
                return None

        def number_expand(tok1, tok2):
            if tok1.tag == tok2.tag == 'number':
                try:
                    new_formula = tok1.formula + tok2.formula
                    new_number = map(lambda a: a if type(a) == str else a.n, new_formula)
                    return Token('number', [Number(' '.join(new_number))])
                except:
                    return Token('number', new_formula)
            else:
                return None

        parser.add_reduce(number_reduce)
        parser.add_expand(number_expand)

        number_jsgf = os.path.join('s2m', 'core', 'sphinx', 'number.jsgf')
        parser.sphinx_config.import_file(number_jsgf)

    @classmethod
    def generate_random(cls) :
        """
        Generates a random instance of Number.
        """
        return Number(numpy.random.randint(0,100000))
