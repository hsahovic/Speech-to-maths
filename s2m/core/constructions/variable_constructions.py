from s2m.core.constructions.constructions import Construction

from s2m.core.utils import reverse_dict


class VariableConstructions(Construction):

    RADIO_ROMAN_PARSED = {'alpha': 'a',
                          'bravo': 'b',
                          'charlie': 'c',
                          'delta': 'd',
                          'echo': 'e',
                          'foxtrot': 'f',
                          'golf': 'g',
                          'hotel': 'h',
                          'india': 'i',
                          'juliett': 'j',
                          'kilo': 'k',
                          'lima': 'l',
                          'mike': 'm',
                          'november': 'n',
                          'oscar': 'o',
                          'papa': 'p',
                          'québec': 'q',
                          'romeo': 'r',
                          'sierra': 's',
                          'tango': 't',
                          'uniform': 'u',
                          'victor': 'v',
                          'whisky': 'w',
                          'xray': 'x',
                          'yankee': 'y',
                          'zulu': 'z'}

    RADIO_ROMAN_REVERSE = reverse_dict(RADIO_ROMAN_PARSED)

    GREEK_PARSED = {'alpha grec': '\\alpha',
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
                    'theta majuscule variante': '\\varTheta',
                    'lambda majuscule': '\\Lambda',
                    'lambda majuscule variante': '\\varLambda',
                    'xi majuscule': '\\Xi',
                    'xi majuscule variante': '\\varXi',
                    'pi majuscule': '\\Pi',
                    'pi majuscule variante': '\\varPi',
                    'sigma majuscule': '\\Sigma',
                    'sigma majuscule variante': '\\varSigma',
                    'upsilon majuscule': '\\Upsilon',
                    'upsilon majuscule variante': '\\varUpsilon',
                    'phi majuscule': '\\Phi',
                    'phi majuscule variante': '\\varPhi',
                    'psi majuscule': '\\Psi',
                    'psi majuscule variante': '\\varPsi',
                    'omega majuscule': '\\Omega',
                    'omega majuscule variante': '\\varOmega',
                    }

    GREEK_REVERSE = reverse_dict(GREEK_PARSED)

    SET_PARSED = {'grand r': '\\mathbb{R}',
                  'grand q': '\\mathbb{Q}',
                  'grand z': '\\mathbb{Z}',
                  'grand n': '\\mathbb{N}',
                  'grand d': '\\mathbb{D}',
                  'grand p': '\\mathbb{P}', }

    SET_REVERSE = reverse_dict(SET_PARSED)

    @classmethod
    def generate_help(cls):
        help = {}
        for (k, v) in cls.RADIO_ROMAN_PARSED.items():
            help[v] = {'name': v,
                       'latex': v,
                       'spelling': k}
        for (k, v) in cls.GREEK_PARSED.items():
            help[k] = {'name': k,
                       'latex': v,
                       'spelling': k}
        for (k, v) in cls.SET_PARSED.items():
            help[k] = {'name': k, 'latex': v, 'spelling': k}
        return help
