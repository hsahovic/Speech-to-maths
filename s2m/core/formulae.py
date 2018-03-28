"""[PSC Speech-to-Math]             (Streichholzschaechtelchen)
                        formulae.py
***************************************************************
*Fournit les structures de base pour l'encodage des arbres    *
*syntaxiques, descendantes de la classe abstraite Formula.    *
*La conversion d'un bloc en code LaTeX est obtenue par appel a*
*la fonction membre latex.                                    * 
*La priorite des operations est prise en compte et le paren-  *
*thesage est ajuste automatiquement en consequence.           *
*Les attributs debutant par un double <i>underscore</i> sont  *
*prives.                                                      *
************************************************************"""

from abc import ABCMeta, abstractmethod
from s2m.core.number_parser import NumberParser
from s2m.core.evaluator import evaluator

import random

class Formula(metaclass=ABCMeta):

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __hash__(self):
        pass

    @abstractmethod
    def _latex(self, next_placeholder=1):
        pass

    @abstractmethod
    def latex(self):
        pass

    @abstractmethod
    def count_brackets(self):
        pass

    @abstractmethod
    def a_similarity(self, f):
        pass

    @abstractmethod
    def d_symmetry(self):
        pass

    @abstractmethod
    def transcription(self):
        pass

    @abstractmethod
    def teach(parser):
        pass

    def brackets_model(self, level):

        if type(level) is not int:
            raise TypeError('Bracket level must be an int, not %r' % i)
        elif level < 1:
            raise ValueError('Bracket level must be non-negative, not %r' % i)
        elif 0 < level < 4:
            return '\\left( %s \\right)'
        elif 4 < level < 6:
            return '\\left[ %s \\right]'
        elif level > 6:
            return '\\left\\lbrace %s \\right\\rbrace'

    def evaluation(self, context_formula=None, placeholder_id=1):

        return evaluator(self, context_formula, placeholder_id)

    def replace_placeholder(self, formula, placeholder_id=0, next_placeholder=1):
        pass

    @abstractmethod
    def tree_depth(self):
        pass
        "renvoie la profondeur (relativement aux feuilles) "
        "à laquelle on se trouve (la racine est de profondeur maximale, "
        "les feuilles sont de profondeur 1)."

    # è_é pas content
    @abstractmethod 
    def extract_3tree(self):
        pass
        "renvoie l'ensemble des 3 arbres présents dans l'arbre synthaxique"

    @abstractmethod
    def count_silsdepths(self):
        pass

    @classmethod
    def generate_random(cls, depth=5):

        from s2m.core.binop import BinaryOperator
        from s2m.core.unop import UnaryOperator
        from s2m.core.number import Number
        from s2m.core.variable import Variable
        from s2m.core.bracketted_block import BrackettedBlock

        subclasses = [UnaryOperator, BinaryOperator, BrackettedBlock]
        subclasses_nodepth = [Number, Variable]

        if depth <= 0:
            return random.choice(subclasses_nodepth).generate_random()
        else:
            return random.choice(subclasses).generate_random(depth=depth-1)

    @classmethod
    def transcription(self):
        pass

   
