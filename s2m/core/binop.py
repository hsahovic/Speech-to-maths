from s2m.core.formulae import Formula
from s2m.core.number import Number
from s2m.core.multiset import Multiset

from s2m.core.utils import merge_lists

from s2m.core.constructions.binop_constructions import BinaryOperatorConstructions

import random

class BinaryOperator(Formula, BinaryOperatorConstructions):

    def __init__(self, l, o, r, ll = False, lr = False):

        if o not in self.operators:
            raise ValueError('Unknown binary operator code : %r' % o)
        elif not issubclass(l.__class__, Formula):
            raise TypeError(
                'LHS of binary operator must be a well-formed formula')
        elif not issubclass(r.__class__, Formula):
            raise TypeError(
                'RHS of binary operator must be a well-formed formula')
        else:
            self.__l, self.__o, self.__r, self.__light_left, self.__light_right = l, o, r, ll, lr

    def __getattr__(self, p):

        if p == 'l':
            return self.__l
        elif p == 'o':
            return self.__o
        elif p == 'r':
            return self.__r
        elif p == 'left_priority':
            if self.__light_left:
                return 0
            else:
                return self.OPERATORS[self.__o]['priority']
        elif p == 'right_priority':
            if self.__light_right:
                return 0
            else:
                return self.OPERATORS[self.__o]['priority']
        elif p == 'priority':
            return self.OPERATORS[self.__o]['priority']
        elif p == 'associative':
            return self.OPERATORS[self.__o]['associative']
        elif p == 'latex_model':
            return self.OPERATORS[self.__o]['latex']
        elif p == 'weak':
            return self.OPERATORS[self.__o]['weak']
        elif p == 'nobrackets':
            return self.OPERATORS[self.__o]['nobrackets']
        elif p == 'operators':
            return self.OPERATORS.keys()
        else:
            raise AttributeError

    def __eq__(self, other):

        if other and isinstance(other, BinaryOperator):
            if other.o == self.__o:
                if self.associative:
                    #workaround! caution!
                    return other.latex() == self.latex()
                else:
                    return other.l == self.__l and other.r == self.__r
        return False

    def __hash__(self):

        return hash(self.__l) ^ hash(self.__o) ^ hash(self.__r)

    def count_brackets(self):
        """Donne le nombre de blocs parentheses et le nombre de blocs non
           parentheses dans le code LaTeX genere"""

        y, n = 0, 0

        if self.__l.priority < self.priority \
           and not self.nobrackets:
            n += 1
        else:
            y += 1

        l_brackets = self.__l.count_brackets()
        y += l_brackets[0]
        n += l_brackets[1]

        if self.__r.priority < self.priority \
           and not self.nobrackets:
            n += 1
        else:
            y += 1

        r_brackets = self.__r.count_brackets()
        y += r_brackets[0]
        n += r_brackets[1]

        return y, n

    def count_silsdepths(self):
        count_sils = 0
        sil_depths = 0
        if self.__l != None:
            sdl, csl = self.__l.count_silsdepths()
            count_sils += csl
            sil_depths += sdl
        if self.__r != None:
            sdr, csr = self.__r.count_silsdepths()
            count_sils += csr
            sil_depths += sdr
        if self.__light_left or self.__light_right:
            count_sils += 1
            sil_depths += self.tree_depth()
        return sil_depths, count_sils

    def flatten(self):
        """Liste les enfants de self dans la representation n-aire minimale"""

        children = []

        if self.__l.__class__ == BinaryOperator \
           and self.__l.priority == self.priority:
            children.extend(self.__l.flatten())
        else:
            children.append(self.__l)

        if self.__r.__class__ == BinaryOperator \
           and self.__r.priority == self.priority:
            children.extend(self.__r.flatten())
        else:
            children.append(self.__r)

        return children

    def a_similarity(self, other):

        if isinstance(other, BinaryOperator) \
           and self.__o == other.o:
            return (self.__l.a_similarity(other.l) \
                    + self.__r.a_similarity(other.r))/2
        else:
            return 0.

    def d_symmetry(self):

        if not self.associative:
            return merge_lists([self.__l.d_symmetry(),
                                self.__r.d_symmetry()],
                               head=self.__l.a_similarity(self.__r))
        else:
            children = self.flatten()
            l = len(children)
            similarities = [children[i].a_similarity(children[j])
                            for i in range(l) for j in range(i + 1, l)]
            avg_similarity = sum(similarities) / len(similarities)
            return merge_lists([child.d_symmetry() for child in children],
                               head=avg_similarity)

    def _latex(self, next_placeholder=1):

        if (self.__l.priority < self.priority
                or (self.__l.priority == self.priority and not self.associative))\
           and not self.nobrackets:
            l_content, next_placeholder, l_level = self.__l._latex(next_placeholder)
            l_level += 1
            l_tex = self.brackets_model(l_level) % l_content
        else:
            l_tex, next_placeholder, l_level = self.__l._latex(next_placeholder)

        if (self.__r.priority < self.priority
                or (self.__r.priority == self.priority and self.weak)) \
                and not self.nobrackets:
            r_content, next_placeholder, r_level = self.__r._latex(next_placeholder)
            r_level += 1
            r_tex = self.brackets_model(r_level) % r_content
        else:
            r_tex, next_placeholder, r_level = self.__r._latex(next_placeholder)

        return self.latex_model % (l_tex, r_tex), next_placeholder, max(l_level, r_level)

    def latex(self):
        """Genere le code LaTeX correspondant a self"""
        return self._latex()[0]

    def transcription(self):

        if self.__o == 'POW' \
           and self.__r.__class__ == Number \
           and self.__r.val == 2:
            return self.__l.transcription() + ' au carré'
        else:
            return '%s %s %s' % (self.__l.transcription(),
                                 self.OPERATORS_REVERSE[self.__o],
                                 self.__r.transcription())

    def replace_placeholder(self, formula, placeholder_id=0, next_placeholder=1, conservative=False):

        next_placeholder = self.__l.replace_placeholder(formula,
                                                        placeholder_id,
                                                        next_placeholder,
                                                        conservative)

        if next_placeholder == 0:
            return 0
        else:
            return self.__r.replace_placeholder(formula,
                                                placeholder_id,
                                                next_placeholder,
                                                conservative)

    def tree_depth(self):
        return 1 + max(self.__r.tree_depth(), self.__l.tree_depth())

    def extract_3tree(self):
        temp_depth = self.tree_depth()
        if temp_depth == 3:
             return Multiset([self])
        elif temp_depth > 3:
            return self.__r.extract_3tree().union(self.__l.extract_3tree())
        else:
            return Multiset()
    
    @classmethod
    def teach(cls, parser):

        binary_operator_easy = ('binaryoperator-operator',
                                cls.OPERATORS_PARSED,
                                lambda x: x)

        # Defines A op B -> BinaryOperator(A, op, B)
        def binary_operator_complex_expand(formulae):
            return BinaryOperator(*formulae)

        binary_operator_complex = ('binaryoperator',
                                   '%f $binaryoperator-operator %f',
                                   binary_operator_complex_expand,
                                   True)

        # Defines A carre -> BinaryOperator(A, 'POW', Number(2))
        def squared_complex_expand(formulae):
            return BinaryOperator(formulae[0], 'POW', Number(2))

        squared_complex = ('binaryoperator/squared',
                           '%f au carré',
                           squared_complex_expand,
                           True)

        # Defines light left and light right operators for silences processing
        def light_left_expand(formulae):
            return BinaryOperator(*formulae, ll = True)

        def light_right_expand(formulae):
            return BinaryOperator(*formulae, lr = True)


        binary_operator_light_left = ('binaryoperator/lightleft',
                                '%f [sil] $binaryoperator-operator %f',
                                light_left_expand,
                                True)

        binary_operator_light_right = ('binaryoperator/lightright',
                                '%f $binaryoperator-operator [sil] %f',
                                light_right_expand,
                                True)

        parser.add_easy_reduce(*binary_operator_easy)
        parser.add_complex_rule(*binary_operator_complex)
        parser.add_complex_rule(*squared_complex)
        parser.add_complex_rule(*binary_operator_light_left)
        parser.add_complex_rule(*binary_operator_light_right)

        BinaryOperatorConstructions.teach(parser)

    @classmethod
    def generate_random(cls, l=None, r=None, depth=1):
        """
        Generates a random instance of BinaryOperator.
        """
        o = random.choice(list(cls.OPERATORS.keys()))
        if l == None:
            l = Formula.generate_random(depth=depth-1)
        if r == None:
            r = Formula.generate_random(depth=depth-1)
        return BinaryOperator(l, o, r)
