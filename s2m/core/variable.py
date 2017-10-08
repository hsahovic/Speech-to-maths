from s2m.core.formulae import Formula
from s2m.core.utils import reverse_dict


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

    __GREEC_PARSED = {'alpha grec': '\alpha',
                      'beta': '\beta',
                      'gamma': '\gamma',
                      'delta grec': '\delta',
                      'epsilon': '\varepsilon',
                      'epsilon variante': '\varepsilon',
                      'zeta': '\zeta',
                      'eta': '\eta',
                      'theta': '\teta',
                      'theta variante': '\vartheta',
                      'iota': '\iota',
                      'kappa': '\kappa',
                      'lambda': '\lambda,
                      'mu': '\mu',
                      'nu': '\nu',
                      'xi': '\xi',
                      'pi': '\pi',
                      'pi variante': '\varpi',
                      'rho': '\rho',
                      'rho variante': '\varrho',
                      'sigma': '\sigma',
                      'sigma variante': '\varsigma',
                      'tau': '\tau',
                      'upsilon': '\upsilon',
                      'phi': '\phi',
                      'phi variante': '\varphi',
                      'chi': '\chi',
                      'psi': '\psi',
                      'omega': '\omega',
                      'gamma majuscule': '\Gamma',
                      'gamma majuscule variante': '\varGamma',
                      'delta majuscule': '\Delta',
                      'delta majuscule variante': '\varDelta',
                      'theta majuscule': '\Theta',
                      'theta majusucle variante': '\varTheta',
                      'lambda majuscule': '\Lambda',
                      'lambda majuscule variante': '\varLambda',
                      'xi majuscule': '\Xi',
                      'xi majuscule variante': '\varXi',
                      'pi majuscule': '\Pi',
                      'pi majuscule variante': '\varPi',
                      'sigma majuscule': '\Sigma',
                      'siigma majuscule variante': '\varSigma',
                      'upsilon majuscule': '\Upsilon',
                      'upsilon majuscule variante': '\varUpsilon',
                      'phi majuscule': '\Phi',
                      'phi majuscule variante': '\varPhi',
                      'psi majuscule': '\Psi',
                      'psi majuscule variante': '\varPsi',
                      'omega majuscule': '\Omega',
                      'omega majusucule variante': '\varOmega',
                      }
    __GREEC_REVERSED = reverse_dict(__GREEC_PARSED)

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
        elif self.__v in self.__GREEC_REVERSED:
            return self.__GREEC_REVERSED[self.__v]
        else:
            raise ValueError('Transcription for variable name %r is not defined.'
                             % self.__v)

    def teach(parser):

        radio_roman_easy_reduce = ('variable-radio-roman',
                                   Variable.__RADIO_ROMAN_PARSED,
                                   lambda x: Variable(x),
                                   True)

        parser.add_easy_reduce(*radio_roman_easy_reduce)
