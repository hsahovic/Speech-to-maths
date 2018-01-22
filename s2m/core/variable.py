from s2m.core.formulae import Formula

from s2m.core.utils import reverse_dict
from s2m.core.utils import merge_lists

import random

class Variable(Formula):

    __RADIO_ROMAN_PARSED = {'alpha': 'a',
                            'bravo': 'b',
                            'charlie': 'c',
                            'delta': 'd',
                            'echo': 'e',
                            'uniform': 'u',
                            'xray': 'x',
                            'yankee': 'y',
                            'zulu': 'z'}

    __RADIO_ROMAN_REVERSE = reverse_dict(__RADIO_ROMAN_PARSED)

    __GREEK_PARSED = {'alpha grec': '\\alpha',
                      'beta': '\\beta',
                      'gamma': '\\gamma',
                      'delta grec': '\\delta',
                      'epsilon': '\\varepsilon',
                      'epsilon variante': '\\varepsilon',
                      'zeta': '\\zeta',
                      'eta': '\\eta',
                      'theta': '\\theta',
                      'theta variante': '\\vartheta',
                      'iota': '\\iota',
                      'kappa': '\\kappa',
                      'lambda': '\\lambda',
                      'mu': '\\mu',
                      'nu': '\\nu',
                      'xi': '\\xi',
                      'pi': '\\pi',
                      'pi variante': '\\varpi',
                      'rho': '\\rho',
                      'rho variante': '\\varrho',
                      'sigma': '\\sigma',
                      'sigma variante': '\\varsigma',
                      'tau': '\\tau',
                      'upsilon': '\\upsilon',
                      'phi': '\\phi',
                      'phi variante': '\\varphi',
                      'chi': '\\chi',
                      'psi': '\\psi',
                      'omega': '\\omega',
                      'gamma majuscule': '\\Gamma',
                      'gamma majuscule variante': '\\varGamma',
                      'delta majuscule': '\\Delta',
                      'delta majuscule variante': '\\varDelta',
                      'theta majuscule': '\\Theta',
                      'theta majusucle variante': '\\varTheta',
                      'lambda majuscule': '\\Lambda',
                      'lambda majuscule variante': '\\varLambda',
                      'xi majuscule': '\\Xi',
                      'xi majuscule variante': '\\varXi',
                      'pi majuscule': '\\Pi',
                      'pi majuscule variante': '\\varPi',
                      'sigma majuscule': '\\Sigma',
                      'siigma majuscule variante': '\\varSigma',
                      'upsilon majuscule': '\\Upsilon',
                      'upsilon majuscule variante': '\\varUpsilon',
                      'phi majuscule': '\\Phi',
                      'phi majuscule variante': '\\varPhi',
                      'psi majuscule': '\\Psi',
                      'psi majuscule variante': '\\varPsi',
                      'omega majuscule': '\\Omega',
                      'omega majuscule variante': '\\varOmega',
                      }
    __GREEK_REVERSE = reverse_dict(__GREEK_PARSED)

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

    def _latex(self):

        return self.__v, 0

    def latex(self):

        return self.__v

    def transcription(self):

        if self.__v in self.__RADIO_ROMAN_REVERSE:
            return self.__RADIO_ROMAN_REVERSE[self.__v]
        elif self.__v in self.__GREEK_REVERSE:
            return self.__GREEK_REVERSE[self.__v]
        else:
            raise ValueError('Transcription for variable name %r is not defined.'
                             % self.__v)

    @classmethod
    def teach(cls, parser):

        radio_roman_easy_reduce = ('variable/radio-roman',
                                   Variable.__RADIO_ROMAN_PARSED,
                                   lambda x: Variable(x),
                                   True)

        parser.add_easy_reduce(*radio_roman_easy_reduce)

    @classmethod
    def generate_random(cls):
        """
        Generates a random variable(either greek or radio)
        """
        
        return Variable(random.choice(list(cls.__GREEK_REVERSE.keys() | cls.__RADIO_ROMAN_REVERSE.keys())))
