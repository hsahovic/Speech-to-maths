from s2m.core.constructions.constructions import Construction

from s2m.core.utils import reverse_dict


class UnaryOperatorConstructions(Construction):

    OPERATORS = {'NEG': {'latex': '-%s', 'priority': 4, 'nobrackets': False},
                 'SQR': {'latex': '\\sqrt{%s}', 'priority': 5, 'nobrackets': True},
                 '3SQ': {'latex': '\\sqrt[3]{%s}', 'priority': 5, 'nobrackets': True},
                 'ABS': {'latex': '\\left| %s \\right|', 'priority': 5, 'nobrackets': True},
                 'FAC': {'latex': '%s!', 'priority': 5, 'nobrackets': True},
                 'CON': {'latex': '\\overline{%s}', 'priority': 5, 'nobrackets': True},
                 'FLO': {'latex': '\\lfloor %s \\rfloor', 'priority': 5, 'nobrackets': True},
                 'INV': {'latex': '%s^{-1}', 'priority': 5, 'nobrackets': True},
                 'STA': {'latex': '%s^{\star}', 'priority': 5, 'nobrackets': True},
                 'TIL': {'latex': '\\tilde{%s}', 'priority': 5, 'nobrackets': True},
                 'HAT': {'latex': '\\hat{%s}', 'priority': 5, 'nobrackets': True},
                 'EXP': {'latex': '\\exp(%s)', 'priority': 5, 'nobrackets': True},
                 'LNN': {'latex': '\\ln(%s)', 'priority': 5, 'nobrackets': True},
                 'SIN': {'latex': '\\sin(%s)', 'priority': 5, 'nobrackets': True},
                 'COS': {'latex': '\\cos(%s)', 'priority': 5, 'nobrackets': True},
                 'TAN': {'latex': '\\tan(%s)', 'priority': 5, 'nobrackets': True},
                 'ARC': {'latex': '\\arccos(%s)', 'priority': 5, 'nobrackets': True},
                 'ARS': {'latex': '\\arcsin(%s)', 'priority': 5, 'nobrackets': True},
                 'ART': {'latex': '\\arctan(%s)', 'priority': 5, 'nobrackets': True},
                 'COH': {'latex': '\\cosh(%s)', 'priority': 5, 'nobrackets': True},
                 'SIH': {'latex': '\\sinh(%s)', 'priority': 5, 'nobrackets': True},
                 'TAH': {'latex': '\\tanh(%s)', 'priority': 5, 'nobrackets': True},
                 'KER': {'latex': '\\ker(%s)', 'priority': 5, 'nobrackets': True},
                 'IMA': {'latex': 'Im(%s)', 'priority': 5, 'nobrackets': True},
                 'ITR': {'latex': '\\overset{\circ}{%s}', 'priority': 5, 'nobrackets': True},
                 'VSN': {'latex': '\\mathcal V (%s)', 'priority': 5, 'nobrackets': True},
                 'ADR': {'latex': '\\overline{%s}', 'priority': 5, 'nobrackets': True},
                 'FTR': {'latex': '\\partial %s ', 'priority': 5, 'nobrackets': True},
                 }

    OPERATORS_PARSED = {'moins': 'NEG',
                        'racine de': 'SQR',
                        'racine carré de': 'SQR',
                        'racine cubique de': '3SQ',
                        'valeur absolu de': 'ABS',
                        'factorielle de': 'FAC',
                        'conjugué de': 'CON',
                        'partie entière de': 'FLO',
                        'inverse de': 'INV',
                        'étoile': 'STA',
                        'tilde': 'TIL',
                        'chapeau': 'HAT',
                        'exponentielle de': 'EXP',
                        'logarithme népérien de': 'LNN',
                        'sinus de': 'SIN',
                        'cosinus de': 'COS',
                        'tangente de': 'TAN',
                        'arc cosinus de': 'ARC',
                        'arc sinus de': 'ARS',
                        'arc tangente de': 'ART',
                        'cosinus hyperbolique de': 'COH',
                        'sinus hyperbolique de': 'SIH',
                        'tangente hyperbolique de': 'COH',
                        'noyau de': 'KER',
                        'image de': 'IMA',
                        'intérieur de': 'ITR',
                        'voisinage de': 'VSN',
                        'adhérence de': 'ADR',
                        'frontière de': 'FTR'}

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
