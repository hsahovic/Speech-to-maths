from s2m.core.constructions.constructions import Construction

from s2m.core.utils import reverse_dict


class UnaryOperatorConstructions(Construction):

    OPERATORS = {'NEG': {'latex': '-%s', 'priority': 4, 'nobrackets': False, 'postfix': False},
                 'SQR': {'latex': '\\sqrt{%s}', 'priority': 5, 'nobrackets': True, 'postfix': False},
                 '3SQ': {'latex': '\\sqrt[3]{%s}', 'priority': 5, 'nobrackets': True, 'postfix': False},
                 'ABS': {'latex': '\\left| %s \\right|', 'priority': 5, 'nobrackets': True, 'postfix': False},
                 'FAC': {'latex': '%s!', 'priority': 5, 'nobrackets': True, 'postfix': False},
                 'CON': {'latex': '\\overline{%s}', 'priority': 5, 'nobrackets': True, 'postfix': False},
                 'FLO': {'latex': '\\lfloor %s \\rfloor', 'priority': 5, 'nobrackets': True, 'postfix': False},
                 'INV': {'latex': '%s^{-1}', 'priority': 5, 'nobrackets': True, 'postfix': True},
                 'STA': {'latex': '%s^{\star}', 'priority': 5, 'nobrackets': True, 'postfix': True},
                 'TIL': {'latex': '\\tilde{%s}', 'priority': 5, 'nobrackets': True, 'postfix': True},
                 'HAT': {'latex': '\\hat{%s}', 'priority': 5, 'nobrackets': True, 'postfix': True},
                 'DOT': {'latex': '\\dot{%s}', 'priority': 5, 'nobrackets': False, 'postfix': True},
                 'DDO': {'latex': '\\ddot{%s}', 'priority': 5, 'nobrackets': False, 'postfix': True},
                 'DDD': {'latex': '\\dddot{%s}', 'priority': 5, 'nobrackets': False, 'postfix': True},
                 'PRM': {'latex': '{%s}^\\prime', 'priority': 5, 'nobrackets': False, 'postfix': True},
                 'PPR': {'latex': '{%s}^{\\prime\\prime}', 'priority': 5, 'nobrackets': False, 'postfix': True},
                 'PPP': {'latex': '{%s}^{\\prime\\prime\\prime}', 'priority': 5, 'nobrackets': False, 'postfix': True},
                 'EXP': {'latex': '\\exp(%s)', 'priority': 5, 'nobrackets': True, 'postfix': False},
                 'LNN': {'latex': '\\ln(%s)', 'priority': 5, 'nobrackets': True, 'postfix': False},
                 'SIN': {'latex': '\\sin(%s)', 'priority': 5, 'nobrackets': True, 'postfix': False},
                 'COS': {'latex': '\\cos(%s)', 'priority': 5, 'nobrackets': True, 'postfix': False},
                 'TAN': {'latex': '\\tan(%s)', 'priority': 5, 'nobrackets': True, 'postfix': False},
                 'ARC': {'latex': '\\arccos(%s)', 'priority': 5, 'nobrackets': True, 'postfix': False},
                 'ARS': {'latex': '\\arcsin(%s)', 'priority': 5, 'nobrackets': True, 'postfix': False},
                 'ART': {'latex': '\\arctan(%s)', 'priority': 5, 'nobrackets': True, 'postfix': False},
                 'COH': {'latex': '\\cosh(%s)', 'priority': 5, 'nobrackets': True, 'postfix': False},
                 'SIH': {'latex': '\\sinh(%s)', 'priority': 5, 'nobrackets': True, 'postfix': False},
                 'TAH': {'latex': '\\tanh(%s)', 'priority': 5, 'nobrackets': True, 'postfix': False},
                 'KER': {'latex': '\\ker(%s)', 'priority': 5, 'nobrackets': True, 'postfix': False},
                 'IMA': {'latex': 'Im(%s)', 'priority': 5, 'nobrackets': True, 'postfix': False},
                 'ITR': {'latex': '\\overset{\circ}{%s}', 'priority': 5, 'nobrackets': True, 'postfix': False},
                 'VSN': {'latex': '\\mathcal V (%s)', 'priority': 5, 'nobrackets': True, 'postfix': False},
                 'ADR': {'latex': '\\overline{%s}', 'priority': 5, 'nobrackets': True, 'postfix': False},
                 'FTR': {'latex': '\\partial %s ', 'priority': 5, 'nobrackets': True, 'postfix': False},
                 'NRM': {'latex': '\\Vert %s \\Vert','priority': 5, 'nobrackets': True, 'postfix': False},
                 'NRO': {'latex': '\\vvvert %s \\vvvert','priority': 5, 'nobrackets': True, 'postfix': False},
                 'EXI': {'latex': '\\exists %s ','priority': 5, 'nobrackets': True, 'postfix': False},
                 'EXU': {'latex': '\\exists ! %s ','priority': 5, 'nobrackets': True, 'postfix': False},
                 'QQS': {'latex': '\\forall %s ','priority': 5, 'nobrackets': True, 'postfix': False}
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
                        'point': 'DOT',
                        'point point': 'DDO',
                        'point point point': 'DDD',
                        'prime': 'PRM',
                        'seconde': 'PPR',
                        'tierce': 'PPP',
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
                        'tangente hyperbolique de': 'TAH',
                        'noyau de': 'KER',
                        'image de': 'IMA',
                        'intérieur de': 'ITR',
                        'voisinage de': 'VSN',
                        'adhérence de': 'ADR',
                        'frontière de': 'FTR',
                        'norme de': 'NRM',
                        'norme subordonnée de': 'NRO',
                        'il existe': 'EXI',
                        'il existe un unique': 'EXU',
                        'quel que soit': 'QQS'}

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
                       'example': ('lambda %s' % n) if v['postfix'] else ('%s lambda' % n),
                       'example-latex': v['latex'] % '\\lambda'}
        return help
