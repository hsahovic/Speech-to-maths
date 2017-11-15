from s2m.core.formulae import Formula
from s2m.core.utils import reverse_dict

import random

class UnaryOperator(Formula):

    __OPERATORS = {'NEG': {'latex': '-%s', 'priority': 4, 'nobrackets': False},
                   'SQR': {'latex': '\\sqrt{%s}', 'priority': 5, 'nobrackets': True},
                   '3SQ': {'latex': '\\sqrt[3]{%s}', 'priority': 5, 'nobrackets': True},
                   'ABS': {'latex': '\\left| %s \\right|', 'priority': 5, 'nobrackets': True}
                   }

    __OPERATORS_PARSED = {'moins': 'NEG',
                          'racine de': 'SQR',
                          'racine carré de': 'SQR',
                          'racine cubique de': '3SQ',
                          'valeur absolu de': 'ABS',
                          }

    __OPERATORS_REVERSE = reverse_dict(__OPERATORS_PARSED)

    def __init__(self, o, r):

        if o not in self.operators:
            raise ValueError('Unknown unary operator code : %r' % o)
        elif not issubclass(r.__class__, Formula):
            raise TypeError(
                'Operand of unary operator must be a well-formed formula')
        else:
            self.__o, self.__r = o, r

    def __getattr__(self, p):

        if p == 'o':
            return self.__o
        elif p == 'r':
            return self.__r
        elif p == 'priority':
            return self.__OPERATORS[self.__o]['priority']
        elif p == 'latex_model':
            return self.__OPERATORS[self.__o]['latex']
        elif p == 'nobrackets':
            return self.__OPERATORS[self.__o]['nobrackets']
        elif p == 'operators':
            return self.__OPERATORS.keys()
        else:
            raise AttributeError

    def __eq__(self, other):
	
        if other and isinstance(other, UnaryOperator):
            return other.o == self.__o and other.r == self.__r
        return False

    def __hash__(self):
        
        return hash(self.__o) ^ hash(self.__r)

    def count_brackets(self):

        y, n = 0, 0

        if self.__r.priority < self.priority \
           and not self.nobrackets:
            n += 1
        else:
            y += 1

        r_brackets = self.__r.count_brackets()
        y += r_brackets[0]
        n += r_brackets[1]

        return y, n

    def distance(self, f):

        if f.__class__ == UnaryOperator:
            if f.o == self.__o:
                return self.__r.distance(f.r)
            else:
                return 1.
        elif issubclass(f.__class__, Formula):
            return 1.
        else:
            raise TypeError('Cannot compare formula with non-formula %r' % f)

    def symmetry_index(self):

        return self.__r.symmetry_index()

    def _latex(self):

        if self.__r.priority < self.priority \
           and not self.nobrackets:
            r_content, r_level = self.__r._latex()
            r_level += 1
            r_tex = self.brackets_model(r_level) % r_content
        else:
            r_tex, r_level = self.__r._latex()

        return self.latex_model % r_tex, r_level

    def latex(self):

        return self._latex()[0]

    def transcription(self):

        if self.__o == 'SQR':
            return 'racine de %s' % self.__r.transcription()
        else:
            return self.__OPERATORS_REVERSE[self.__o] + ' ' + self.__r.transcription()

    def teach(parser):

        # Recognizes unary operators
        unary_operator_easy = ('unaryoperator-operator',
                               UnaryOperator.__OPERATORS_PARSED,
                               lambda x: x)

        # Defines op A -> UnaryOperator(op, A)
        def unary_operator_complex_expand(words):
            return UnaryOperator(words[0], words[1])

        unary_operator_complex = ('unaryoperator',
                                  '$unaryoperator-operator %f',
                                  unary_operator_complex_expand,
                                  True)

        parser.add_easy_reduce(*unary_operator_easy)
        parser.add_complex_rule(*unary_operator_complex)

    @classmethod
    def generate_random(cls,r=None,depth=1) :
        """
        Generates a random instance of UnaryOperator.
        """
        o = random.choice(list(cls.__OPERATORS.keys()))        
        if r == None:
            r=Formula.generate_random(depth=depth)
        return UnaryOperator(o,r)