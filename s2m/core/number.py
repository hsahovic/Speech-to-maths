from s2m.core.formulae import Formula
from s2m.core.variable import Variable
from s2m.core.number_parser import NumberParser

from s2m.core.utils import merge_lists

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

    def a_similarity(self, other):

        from s2m.core.variable import Variable
        
        if isinstance(other, Number):
            return 1.
        elif isinstance(other, Variable):
            return 0.5
        else:
            return 0.

    def d_symmetry(self):

        return merge_lists([], head=1.)

    def _latex(self, next_placeholder=1):

        return repr(self.__val), next_placeholder, 0

    def latex(self):

        return repr(self.__val)

    def transcription(self):

        np = NumberParser()
        return np.transcribe(self.val)

    def replace_placeholder(self, formula, placeholder_id=0, next_placeholder=1):

        return next_placeholder

    @classmethod
    def teach(cls, parser):

        def build_word_string(words):

            word_string = []
            for word in words:
                if isinstance(word, Number):
                    word_string.append(word.n)
                elif type(word) is str:
                    word_string.append(word)
                else:
                    raise TypeError('Words in list should be Number or str, not %r' % type(word))
            return word_string
        
        def number_expand(words):

            word_string = build_word_string(words)
            try:
                return Number(' '.join(word_string))
            except ValueError:
                return word_string

        def number_expand_final(words):

            word_string = build_word_string(words)
            return Number(' '.join(word_string))
            
        def number_reduce(word):
            try:
                return Number(word)
            except ValueError:
                return word

        parser.add_complex_rule('number-prefix',
                                '$number-prefix $number-prefix',
                                number_expand,
                                False)

        parser.add_complex_rule('number',
                                '$number-prefix $number-prefix',
                                number_expand_final,
                                True)

        parser.add_easy_reduce('number-prefix/reduce',
                               {x: x for x in NumberParser.NUMBER_WORDS},
                               number_reduce,
                               False)

        parser.add_easy_reduce('number/reduce',
                               {x: x for x in NumberParser.AUTONOMOUS_NUMBER_WORDS},
                               number_reduce,
                               True)

        number_jsgf = os.path.join('s2m', 'core', 'sphinx', 'number.jsgf')
        parser.sphinx_config.import_file(number_jsgf)

    @classmethod
    def generate_random(cls) :
        """
        Generates a random instance of Number.
        """
        return Number(numpy.random.randint(0,100000))
