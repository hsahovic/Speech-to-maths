#### EN DÉVELOPPEMENT ####
###
from functools import reduce

from s2m.core.formulae import Formula
from s2m.core.multiset import Multiset

from s2m.core.constructions.bigop_constructions import BigOperatorConstructions

import random


class BigOperator(Formula, BigOperatorConstructions):

    def __init__(self, o, *args):  # EN CONSTRUCTION !! ## à adapter avec args
        if o not in self.operators:
            raise ValueError('Unknown big operator code : %r' % o)
        if self.OPERATORS[o]['type'] == 'SUM':
            if len(args) > 3 or len(args) == 0:
                raise ValueError(
                    'Wrong amout of arguments for operator: %r' % len(args))
        elif self.OPERATORS[o]['type'] == 'ITV':
            if len(args) > 4 or len(args) < 3:
                raise ValueError(
                    'Wrong amout of arguments for operator: %r' % len(args))
        elif self.OPERATORS[o]['type'] == 'DEV':
            if len(args) > 3 or len(args) == 0:
                raise ValueError(
                    'Wrong amout of arguments for operator: %r' % len(args))
        self.__fl = args
        self.__o = o

    def __getattr__(self, p):
        if p == 'o':
            return self.__o
        elif p == 'fl':
            return self.__fl
        elif p == 'priority':
            return self.OPERATORS[self.__o]['priority']
        elif p == 'latex_model':
            return self.OPERATORS[self.__o]['latex']
        elif p == 'operator_type':
            return self.OPERATORS[self.__o]['type']
        elif p == 'arity':
            return len(self.__fl)
        elif p == 'operators':
            return self.OPERATORS.keys()
        else:
            raise AttributeError

    def __eq__(self, other):
        if other and isinstance(other, BigOperator):
            if other.o == self.__o and other.arity == self.arity:
                for i, form in enumerate(self.__fl):
                    if form != other.fl[i]:
                        return False
                else:
                    return True
        return False

    def __hash__(self):
        return reduce(lambda a, b: a ^ hash(b), self.__fl, 0)

    def _latex(self, next_placeholder=1):
        from s2m.core.number import Number
        if self.operator_type == 'SUM':
            c_tex, c_level = '', 0
            d_tex, d_level = '', 0
            u_tex, u_level = '', 0
            if len(self.__fl) == 1:
                c_tex, next_placeholder, c_level = self.__fl[0]._latex(
                    next_placeholder)
            elif len(self.__fl) == 2:
                c_tex, next_placeholder, c_level = self.__fl[1]._latex(
                    next_placeholder)
                d_tex, next_placeholder, d_level = self.__fl[0]._latex(
                    next_placeholder)
            elif len(self.__fl) == 3:
                c_tex, next_placeholder, c_level = self.__fl[2]._latex(
                    next_placeholder)
                d_tex, next_placeholder, d_level = self.__fl[0]._latex(
                    next_placeholder)
                u_tex, next_placeholder, u_level = self.__fl[1]._latex(
                    next_placeholder)
            return (self.latex_model % (d_tex, u_tex, c_tex),
                    next_placeholder,
                    c_level)
        elif self.operator_type == 'ITV':
            lb_tex = self.BOUNDS[(self.__o, self.__fl[0], 0)]
            l_tex, next_placeholder, l_level = self.__fl[1]._latex(
                    next_placeholder)
            if len(self.__fl) == 3:
                rb_tex = self.BOUNDS[(self.__o, self.__fl[0], 1)]
                r_tex, next_placeholder, r_level = self.__fl[2]._latex(
                    next_placeholder)
            elif len(self.__fl) == 4:
                rb_tex = self.BOUNDS[(self.__o, self.__fl[2], 1)]
                r_tex, next_placeholder, r_level = self.__fl[3]._latex(
                    next_placeholder)
            return (self.latex_model % (lb_tex, l_tex, r_tex, rb_tex),
                    next_placeholder,
                    max(l_level, r_level))
        elif self.operator_type == 'DEV':
            c_tex, c_level = '', 0
            d_tex, d_level = '', 0
            u_tex, u_level = '', 0
            if len(self.__fl) == 1:
                c_tex, next_placeholder, c_level = self.__fl[0]._latex(
                    next_placeholder)
            elif len(self.__fl) == 2:
                c_tex, next_placeholder, c_level = self.__fl[1]._latex(
                    next_placeholder)
                u_tex, next_placeholder, u_level = self.__fl[0]._latex(
                    next_placeholder)
            elif len(self.__fl) == 3:
                c_tex, next_placeholder, c_level = self.__fl[2]._latex(
                    next_placeholder)
                u_tex, next_placeholder, u_level = self.__fl[0]._latex(
                    next_placeholder)
                d_tex, next_placeholder, d_level = self.__fl[1]._latex(
                    next_placeholder)
            if u_tex == Number(1).latex():
                u_tex = ''
            return (self.latex_model % (d_tex, u_tex, c_tex),
                    next_placeholder,
                    c_level)
        else:
            return '', next_placeholder, 0

    def latex(self):
        """Genere le code LaTeX correspondant a self"""
        return self._latex()[0]

    def count_brackets(self):
        return self.__fl[-1].count_brackets()

    def count_silsdepths(self):
        return self.__fl[-1].count_silsdepths()

    def a_similarity(self, other):
        if isinstance(other, BigOperator) \
           and self.__o == other.o \
           and self.arity == other.arity:
            s = 0
            for i in range(self.arity):
                s += (self.__fl[i]).a_similarity(other.fl[i])
            return s / self.arity
        else:
            return 0.

    def d_symmetry(self):
        return self.__fl[-1].d_symmetry()

    def replace_placeholder(self, formula, placeholder_id=0, next_placeholder=1, conservative=False):
        for (i, f) in enumerate(self.__fl):
            next_placeholder = f.replace_placeholder(formula,
                                                     placeholder_id,
                                                     next_placeholder,
                                                     conservative)
            if next_placeholder == 0:
                return 0
        return next_placeholder

    def tree_depth(self):
        return 1 + max([self.__fl[i].tree_depth() for i in range (self.__fl).length()])

    def extract_3tree(self):
        temp_depth = self.tree_depth()
        if temp_depth == 3:
            return Multiset([self])
        elif temp_depth > 3:
            return Multiset().union(*[self.__fl[i].extract_3tree() for i in range(self.__fl.length())])
        else:
            return Multiset()
    

    @classmethod
    def teach(cls, parser):

        from s2m.core.number import Number

        big_operator_easy = ('bigoperator-operator',
                             cls.OPERATORS_PARSED,
                             lambda x: x)

        big_operator_from = ('bigoperator-from',
                             {'de': None, 'pour': None, 'sur': None},
                             lambda x: None)

        big_operator_of = ('bigoperator-of',
                           {'de': None, 'des': None},
                           lambda x: None)

        big_operator_bnd = ('bigoperator-bnd',
                            cls.BOUNDS_PARSED,
                            lambda x: x)

        # Defines op A -> BigOperator(op, A)
        def big_operator_expand(formulae):
            return BigOperator(*[f for f in formulae if f is not None])

        big_operator_arity1_complex = ('bigoperator/arity1',
                                       '$bigoperator-operator $bigoperator-of %f',
                                       big_operator_expand,
                                       True)

        # Defines op from A of B -> BigOperator(op, A, B)
        big_operator_arity2_complex = ('bigoperator/arity2',
                                       '$bigoperator-operator $bigoperator-from %f $bigoperator-of %f',
                                       big_operator_expand,
                                       True)

        # Defines op from A to B of C -> BigOperator(op, A, B, C)
        big_operator_arity3_complex = ('bigoperator/arity3',
                                       '$bigoperator-operator $bigoperator-from %f à %f $bigoperator-of %f',
                                       big_operator_expand,
                                       True)

        # Defines op bnd from A to B -> BigOperator(op, bnd, A, B)
        itv_arity3_complex = ('bigoperator/itvarity3',
                             '$bigoperator-operator $bigoperator-bnd de %f à %f',
                             big_operator_expand)

        # Defines op bndA in A bndB in B -> BigOperator(op, bnd, A, bnd, B)
        itv_arity4_complex = ('bigoperator/itvarity4',
                             '$bigoperator-operator $bigoperator-bnd en %f $bigoperator-bnd en %f',
                             big_operator_expand)

        # Interval shortcuts
        segment_complex = ('bigoperator/segment',
                                    'segment de %f à %f',
                                    lambda x: big_operator_expand(['ITR', 'CL', x[0], x[1]]),
                                    True)

        interval_complex = ('bigoperator/interval',
                                    'intervalle de %f à %f',
                                    lambda x: big_operator_expand(['ITR', 'OP', x[0], x[1]]),
                                    True)

        # Derivatives
        derivative_arity1_complex = ('bigoperator/devarity1',
                                     '$bigoperator-operator %f',
                                     big_operator_expand,
                                     True)

        derivative_arity2_complex = ('bigoperator/devarity2',
                                     '$bigoperator-operator par rapport à %f de %f',
                                     lambda x: big_operator_expand([x[0], Number(1), x[1], x[2]]),
                                     True)

        derivative_arity2b_complex = ('bigoperator/devarity2b',
                                     '$bigoperator-operator %f %f',
                                     big_operator_expand,
                                     True)

        derivative_arity3_complex = ('bigoperator/devarity3',
                                     '$bigoperator-operator %f par rapport à %f de %f',
                                     big_operator_expand,
                                     True)

        parser.add_easy_reduce(*big_operator_easy)
        parser.add_easy_reduce(*big_operator_from)
        parser.add_easy_reduce(*big_operator_of)
        parser.add_easy_reduce(*big_operator_bnd)
        parser.add_complex_rule(*big_operator_arity1_complex)
        parser.add_complex_rule(*big_operator_arity2_complex)
        parser.add_complex_rule(*big_operator_arity3_complex)
        parser.add_complex_rule(*itv_arity3_complex)
        parser.add_complex_rule(*itv_arity4_complex)
        parser.add_complex_rule(*segment_complex)
        parser.add_complex_rule(*interval_complex)
        parser.add_complex_rule(*derivative_arity1_complex)
        parser.add_complex_rule(*derivative_arity2_complex)
        parser.add_complex_rule(*derivative_arity2b_complex)
        parser.add_complex_rule(*derivative_arity3_complex)

        BigOperatorConstructions.teach(parser)

    def transcription(self):

        from s2m.core.number import Number
        
        if self.operator_type == 'SUM':
            if self.__o == 'ITG':
                connector = 'de'
            else:
                connector = 'des'
            if len(self.__fl) == 1:
                return '%s %s %s' % (self.OPERATORS_REVERSE[self.__o],
                                     connector,
                                     self.__fl[0].transcription())
            elif len(self.__fl) == 2:
                return '%s sur %s %s %s' % (self.OPERATORS_REVERSE[self.__o],
                                            self.__fl[0].transcription(),
                                            connector,
                                            self.__fl[1].transcription())
            else:
                return '%s de %s à %s %s %s' % (self.OPERATORS_REVERSE[self.__o],
                                                self.__fl[0].transcription(),
                                                self.__fl[1].transcription(),
                                                connector,
                                                self.__fl[2].transcription())
        if self.operator_type == 'ITV':
            if len(self.__fl) == 3:
                return '%s %s de %s à %s' % (self.OPERATORS_REVERSE[self.__o],
                                             self.BOUNDS_REVERSE[self.__fl[0]],
                                             self.__fl[1].transcription(),
                                             self.__fl[2].transcription())
            else: 
                return '%s %s en %s %s en %s' % (self.OPERATORS_REVERSE[self.__o],
                                                 self.BOUNDS_REVERSE[self.__fl[0]],
                                                 self.__fl[1].transcription(),
                                                 self.BOUNDS_REVERSE[self.__fl[2]],
                                                 self.__fl[3].transcription())
        if self.operator_type == 'DEV':
            if len(self.__fl) == 1:
                return '%s %s' % (self.OPERATORS_REVERSE[self.__o],
                                     self.__fl[0].transcription())
            elif len(self.__fl) == 2:
                return '%s %s %s' % (self.OPERATORS_REVERSE[self.__o],
                                     self.__fl[0].transcription(),
                                     self.__fl[1].transcription())
            else:
                if self.__fl[0] == Number(1):
                    return '%s par rapport à %s de %s' % (self.OPERATORS_REVERSE[self.__o],
                                                          self.__fl[1].transcription(),
                                                          self.__fl[2].transcription())
                else:
                    return '%s %s par rapport à %s de %s' % (self.OPERATORS_REVERSE[self.__o],
                                                             self.__fl[0].transcription(),
                                                             self.__fl[1].transcription(),
                                                             self.__fl[2].transcription())
