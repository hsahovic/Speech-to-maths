from s2m.core.formulae import Formula
from s2m.core.utils import reverse_dict

class Variable(Formula):

    __RADIO_ROMAN_PARSED = {'alpha':'a',
                            'bravo':'b',
                            'charlie':'c',
                            'delta':'d',
                            'echo':'e',
                            'uniform':'u',
                            'xray':'x',
                            'yankee':'y',
                            'zulu':'z'}
    
    __RADIO_ROMAN_REVERSE = reverse_dict(__RADIO_ROMAN_PARSED)
    
    def __init__(self, v):

        if type(v) is not str:
            raise TypeError('Variable identifier must be a string, not %r' % v)
        else:
            self.__v = v

    def __getattr__(self, p):

        if p == 'v':
            return self.__v
        elif p == 'priority':
            return 5
        else:
            raise AttributeError

    def count_brackets(self):

        return 0, 0

    def distance(self, f):

        from s2m.core.number import Number

        if f.__class__ == Variable:
            return 0.
        elif f.__class__ == Number:
            return 0.5
        elif issubclass(f.__class__, Formula):
            return 1.
        else:
            raise TypeError('Cannot compare Variable to non-formula %r' % f)

    def symmetry_index(self):

        return 1.

    def _latex(self):

        return self.__v, 0

    def latex(self):

        return self.__v

    def transcription(self):

        if self.__v in self.__RADIO_ROMAN_REVERSE:
            return self.__RADIO_ROMAN_REVERSE[self.__v]
        else:
            raise ValueError('Transcription for variable name %r is not defined.'
                             % self.__v)
                
    def teach(parser):

        radio_roman_easy_reduce = ('variable-radio-roman',
                                   Variable.__RADIO_ROMAN_PARSED,
                                   lambda x: Variable(x),
                                   True)

        parser.add_easy_reduce(*radio_roman_easy_reduce)
