from s2m.core.formulae import Formula

from s2m.core.utils import merge_lists

from s2m.core.constructions.variable import VariableConstructions

import random

class Variable(Formula, VariableConstructions):

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

    def __eq__(self, other):

        if other and isinstance(other, Variable):
            return other.v == self.__v
        return False

    def __hash__(self):

        return hash(self.__v)

    def count_brackets(self):

        return 0, 0

    def a_similarity(self, other):

        from s2m.core.number import Number

        if isinstance(other, Variable):
            return 1.
        elif isinstance(other, Number):
            return 0.5
        else:
            return 0.

    def d_symmetry(self):

        return merge_lists([], head=1.)

    def _latex(self, next_placeholder=1):

        return self.__v, next_placeholder, 0

    def latex(self):

        return self.__v

    def transcription(self):

        if self.__v in self.RADIO_ROMAN_REVERSE:
            return self.RADIO_ROMAN_REVERSE[self.__v]
        elif self.__v in self.GREEK_REVERSE:
            return self.GREEK_REVERSE[self.__v]
        else:
            raise ValueError('Transcription for variable name %r is not defined.'
                             % self.__v)

    def replace_placeholder(self, formula, placeholder_id=0, next_placeholder=1):

        return next_placeholder

    @classmethod
    def teach(cls, parser):

        radio_roman_easy_reduce = ('variable/radio-roman',
                                   Variable.RADIO_ROMAN_PARSED,
                                   lambda x: Variable(x),
                                   True)

        greek_easy_reduce = ('variable/greek',
                             Variable.GREEK_PARSED,
                             lambda x: Variable(x),
                             True)

        parser.add_easy_reduce(*radio_roman_easy_reduce)
        parser.add_easy_reduce(*greek_easy_reduce)

        VariableConstructions.teach(parser)

    @classmethod
    def generate_random(cls):
        """
        Generates a random variable(either greek or radio)
        """

        return Variable(random.choice(list(cls.GREEK_REVERSE.keys() | cls.RADIO_ROMAN_REVERSE.keys())))
