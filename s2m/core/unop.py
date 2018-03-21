from s2m.core.formulae import Formula

from s2m.core.utils import merge_lists

from s2m.core.constructions.unop_constructions import UnaryOperatorConstructions

import random


class UnaryOperator(Formula, UnaryOperatorConstructions):

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
            return self.OPERATORS[self.__o]['priority']
        elif p == 'latex_model':
            return self.OPERATORS[self.__o]['latex']
        elif p == 'nobrackets':
            return self.OPERATORS[self.__o]['nobrackets']
        elif p == 'operators':
            return self.OPERATORS.keys()
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

    def a_similarity(self, other):
        if isinstance(other, UnaryOperator) \
           and self.__o == other.o:
            return self.__r.a_similarity(other.r)
        else:
            return 0.

    def d_symmetry(self):
        return self.__r.d_symmetry()

    def _latex(self, next_placeholder=1):
        if self.__r.priority < self.priority \
           and not self.nobrackets:
            r_content, next_placeholder, r_level = self.__r._latex(
                next_placeholder)
            r_level += 1
            r_tex = self.brackets_model(r_level) % r_content
        else:
            r_tex, next_placeholder, r_level = self.__r._latex(
                next_placeholder)

        return self.latex_model % r_tex, next_placeholder, r_level

    def latex(self):
        return self._latex()[0]

    def transcription(self):
        if self.__o == 'SQR':
            return 'racine de %s' % self.__r.transcription()
        else:
            return self.OPERATORS_REVERSE[self.__o] + ' ' + self.__r.transcription()

    def replace_placeholder(self, formula, placeholder_id=0, next_placeholder=1, conservative=False):
        return self.__r.replace_placeholder(formula, placeholder_id, next_placeholder, conservative)

    def tree_depth(self):
<<<<<<< HEAD
        return 1+self.__r.tree_depth()
    
     def extract_3tree(self):
        temp_depth=self.tree_depth
        if temp_depth==3:
             return set(self)
        elif temp_depth>3:
            return return self.__r.extract_3tree()
=======
        return 1 + self.__r.tree_depth()

    def extract_3tree(self):
        temp_depth = self.tree_depth
        if temp_depth == 3:
            return set(self)
        elif temp_depth > 3:
            return self.__r.extract_3tree()
>>>>>>> 8f5a4c85635d556366224a7629f98c5e0eef8e4d
        else:
            return set()

    @classmethod
    def teach(cls, parser):
        # Recognizes unary operators
        unary_operator_easy = ('unaryoperator-operator',
                               cls.OPERATORS_PARSED,
                               lambda x: x)

        # Recognized unary operators without 'de'
        unary_operator_term_easy = ('unaryoperator-term',
                                    {k[:k.rfind(' ') if k.rfind(' ') >= 0 else len(k)]: v
                                     for (k, v) in cls.OPERATORS_PARSED.items()},
                                    lambda x: x)

        # Defines op A -> UnaryOperator(op, A)
        def unary_operator_complex_expand(words):
            return UnaryOperator(*words)
        unary_operator_complex = ('unaryoperator',
                                  '$unaryoperator-operator %f',
                                  unary_operator_complex_expand,
                                  True)

        # Defines op A fin de op -> UnaryOperator(op, A)
        def unary_operator_explicit_complex_expand(words):
            if len(words) == 3 and words[0] == words[2]:
                return UnaryOperator(*words[:2])
            else:
                raise Exception

        unary_operator_explicit_complex = ('unaryoperator/explicit',
                                           '$unaryoperator-operator %f fin de $unaryoperator-term',
                                           unary_operator_explicit_complex_expand,
                                           True)

        parser.add_easy_reduce(*unary_operator_term_easy)
        parser.add_easy_reduce(*unary_operator_easy)
        parser.add_complex_rule(*unary_operator_complex)
        parser.add_complex_rule(*unary_operator_explicit_complex)

        UnaryOperatorConstructions.teach(parser)

    @classmethod
    def generate_random(cls, r=None, depth=1):
        """
        Generates a random instance of UnaryOperator.
        """
        o = random.choice(list(cls.OPERATORS.keys()))
        if r == None:
            r = Formula.generate_random(depth=depth - 1)
        return UnaryOperator(o, r)
