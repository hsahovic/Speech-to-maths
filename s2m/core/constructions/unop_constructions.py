from s2m.core.constructions.constructions import Construction

from s2m.core.utils import reverse_dict

class UnaryOperatorConstructions(Construction):

    OPERATORS = {'NEG': {'latex': '-%s', 'priority': 4, 'nobrackets': False},
                 'SQR': {'latex': '\\sqrt{%s}', 'priority': 5, 'nobrackets': True},
                 '3SQ': {'latex': '\\sqrt[3]{%s}', 'priority': 5, 'nobrackets': True},
                 'ABS': {'latex': '\\left| %s \\right|', 'priority': 5, 'nobrackets': True}}

    OPERATORS_PARSED = {'moins': 'NEG',
                        'racine de': 'SQR',
                        'racine carré de': 'SQR',
                        'racine cubique de': '3SQ',
                        'valeur absolu de': 'ABS'}

    OPERATORS_REVERSE = reverse_dict(OPERATORS_PARSED)

    @classmethod
    def generate_help(cls):
        BLANK = '\\bullet'
        help = {}
        for (k, v) in cls.OPERATORS.items():
            n = cls.OPERATORS_REVERSE[k]
            help[n] = {'name': ' '.join(n.split(' ')[:(len(n)-1 or 1)]),
                       'latex': v['latex'] % BLANK,
                       'spelling': n,
                       'example': '%s lambda' % n,
                       'example-latex': v['latex'] % '\\lambda'}
        return help
