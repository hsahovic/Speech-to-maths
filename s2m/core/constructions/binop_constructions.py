from s2m.core.constructions.constructions import Construction

from s2m.core.utils import reverse_dict


class BinaryOperatorConstructions(Construction):

    OPERATORS = {'EQU': {'latex': '%s = %s', 'priority': 0, 'associative': True, 'weak': False, 'nobrackets': True},
                 'NEQ': {'latex': '%s \\neq %s', 'priority': 0, 'associative': True, 'weak': False, 'nobrackets': False},
                 'GEQ': {'latex': '%s \\geq %s', 'priority': 0, 'associative': True, 'weak': False, 'nobrackets': False},
                 'LEQ': {'latex': '%s \\leq %s', 'priority': 0, 'associative': True, 'weak': False, 'nobrackets': False},
                 'EQV': {'latex': '%s \\sim %s', 'priority': 0, 'associative': True, 'weak': False, 'nobrackets': False},
                 'SEQ': {'latex': '%s \\simeq %s', 'priority': 0, 'associative': True, 'weak': False, 'nobrackets': False},
                 'SBS': {'latex': '%s \\subset %s', 'priority': 0, 'associative': True, 'weak': False, 'nobrackets': False},
                 'SPS': {'latex': '%s \\supset %s', 'priority': 0, 'associative': True, 'weak': False, 'nobrackets': False},
                 'ADD': {'latex': '%s + %s', 'priority': 1, 'associative': True, 'weak': False, 'nobrackets': False},
                 'SUB': {'latex': '%s - %s', 'priority': 1, 'associative': False, 'weak': True, 'nobrackets': False},
                 'PMS': {'latex': '%s \\pm %s', 'priority': 1, 'associative': True, 'weak': True, 'nobrackets': False},
                 'MPS': {'latex': '%s \\mp %s', 'priority': 1, 'associative': True, 'weak': True, 'nobrackets': False},
                 'MUL': {'latex': '%s \\times %s', 'priority': 2, 'associative': True, 'weak': False, 'nobrackets': False},
                 'DIV': {'latex': '\\frac{%s}{%s}', 'priority': 2, 'associative': False, 'weak': False, 'nobrackets': True},
                 'CMP': {'latex': '%s \\circ %s', 'priority': 2, 'associative': True, 'weak': False, 'nobrackets': False},
                 'VEC': {'latex': '%s \\wedge %s', 'priority': 2, 'associative': True, 'weak': False, 'nobrackets': False},
                 'POW': {'latex': '{%s}^{%s}', 'priority': 3, 'associative': False, 'weak': False, 'nobrackets': False},
                 'EVL': {'latex': '%s \\left( %s \\right)', 'priority': 4, 'associative': False, 'weak': False, 'nobrackets': True},
                 'BIN': {'latex': '\\binom {%s} {%s}', 'priority': 4, 'associative': False, 'weak': False, 'nobrackets': True},
                 'BEL': {'latex': '%s \\in %s', 'priority': 0, 'associative': True, 'weak': False, 'nobrackets': False},
                 'NBL': {'latex': '%s \\notin %s', 'priority': 0, 'associative': True, 'weak': False, 'nobrackets': False},
                 'PRI': {'latex': '%s \\setminus %s', 'priority': 0, 'associative': True, 'weak': False, 'nobrackets': False},
                 'UNI': {'latex': '%s \\cup %s', 'priority': 0, 'associative': True, 'weak': False, 'nobrackets': False},
                 'INT': {'latex': '%s \\cap %s', 'priority': 0, 'associative': True, 'weak': False, 'nobrackets': False},
                 'SYM': {'latex': '%s \\oplus %s', 'priority': 0, 'associative': True, 'weak': False, 'nobrackets': False},
                 'DST': {'latex': 'd ( %s , %s )', 'priority': 0, 'associative': False, 'weak': False, 'nobrackets': True},
                 'BLO': {'latex': 'B ( %s , %s )', 'priority': 0, 'associative': False, 'weak': False, 'nobrackets': True},
                 'BLF': {'latex': 'B_f ( %s , %s )', 'priority': 0, 'associative': False, 'weak': False, 'nobrackets': True},
                 'DVS': {'latex': '%s \\mid  %s', 'priority': 0, 'associative': False, 'weak': False, 'nobrackets': True},
                 'NDV': {'latex': '%s \\nmid %s', 'priority': 0, 'associative': False, 'weak': False, 'nobrackets': True},
                 'MOD': {'latex': '%s \\pmod{%s} ', 'priority': 0, 'associative': False, 'weak': False, 'nobrackets': True},
                 'CGR': {'latex': '%s \\equiv %s ', 'priority': 0, 'associative': False, 'weak': False, 'nobrackets': True},
                 'GCD': {'latex': '%s \\wedge %s ', 'priority': 0, 'associative': True, 'weak': False, 'nobrackets': True},
                 'LCM': {'latex': '%s \\vee %s ', 'priority': 0, 'associative': True, 'weak': False, 'nobrackets': True}
                 }

    OPERATORS_PARSED = {'plus': 'ADD',
                        'moins': 'SUB',
                        'fois': 'MUL',
                        'sur': 'DIV',
                        'divisé par': 'DIV',
                        'puissance': 'POW',
                        'égal': 'EQU',
                        'différent de': 'NEQ',
                        'supérieur à': 'GEQ',
                        'inférieur à': 'LEQ',
                        'plus ou moins': 'PMS',
                        'moins ou plus': 'MPS',
                        'rond': 'CMP',
                        'vectoriel': 'VEC',
                        'inclus dans': 'SBS',
                        'contient': 'SPS',
                        'équivaut à': 'EQV',
                        'environ égal à': 'SEQ',
                        'de': 'EVL',
                        'binomial': 'BIN',
                        'appartient à': 'BEL',
                        "nappartient pas à": 'NBL',
                        'privé de': 'PRI',
                        'union': 'UNI',
                        'intersection': 'INT',
                        'différence symétrique': 'SYM',
                        'distance': 'DST',
                        'boule ouverte ': 'BLO',
                        'boule fermée ': 'BLF',
                        'divise ': 'DVS',
                        'ne divise pas ': 'NDV',
                        'modulo ': 'MOD',
                        'congru à ': 'CGR',
                        'pgcd ': 'GCD',
                        'ppcm ': 'LCM'
                        }

    OPERATORS_REVERSE = reverse_dict(OPERATORS_PARSED)

    @classmethod
    def generate_help(cls):
        BLANK = ('\\bullet', '\\bullet')
        help = {}
        for (k, v) in cls.OPERATORS.items():
            n = cls.OPERATORS_REVERSE[k]
            help[n] = {'name': n,
                       'latex': v['latex'] % BLANK,
                       'spelling': n,
                       'example': 'lambda %s mu' % n,
                       'example-latex': v['latex'] % ('\\lambda', '\\mu')}
        return help
