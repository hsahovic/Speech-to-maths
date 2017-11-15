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
from s2m.core.parser import Token

import random

class Formula(metaclass=ABCMeta):

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __hash__(self):
        pass

    @abstractmethod
    def _latex(self):
        pass

    @abstractmethod
    def latex(self):
        pass

    @abstractmethod
    def count_brackets(self):
        pass

    def natural_bracketting_index(self):
        """Donne la proportion de blocs parentheses dans le code LaTeX
           parmi l'ensemble des blocs generes"""

        brackets = self.count_brackets()
        if brackets[0] == brackets[1] == 0:
            return 1.
        else:
            return float(brackets[0]) / (brackets[0] + brackets[1])

    @abstractmethod
    def distance(self, f):
        pass

    @abstractmethod
    def symmetry_index(self):
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
