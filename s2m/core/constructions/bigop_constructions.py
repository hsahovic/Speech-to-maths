from s2m.core.constructions.constructions import Construction

from s2m.core.utils import reverse_dict


class BigOperatorConstructions(Construction):

    OPERATORS = {'ITG': {'latex': '\\int_{%s}^{%s} %s', 'priority': 1, 'type': 'SUM', 'subtype': 'CON'},
                 'SUM': {'latex': '\\sum_{%s}^{%s} %s', 'priority': 1, 'type': 'SUM', 'subtype': 'DIS'},
                 'PRO': {'latex': '\\prod_{%s}^{%s} %s', 'priority': 2, 'type': 'SUM', 'subtype': 'DIS'},
                 'ITR': {'latex': '\bigcap_{%s}^{%s} %s', 'priority': 2, 'type': 'SUM', 'subtype': 'DIS'},
                 'UNI': {'latex': '\bigcup_{%s}^{%s} %s', 'priority': 1, 'type': 'SUM', 'subtype': 'DIS'},
                 'LIM': {'latex': '\\underset{ %s \\rightarrow \%s}{\\lim} %s ', 'priority': 1, 'type': 'LIM', 'subtype': 'LIM'},
                 }

    OPERATORS_PARSED = {'intégrale': 'ITG',
                        'somme': 'SUM',
                        'produit': 'PRO',
                        'intersection': 'ITR',
                        'union': 'UNI',
                        'limite': 'LIM'
                        }

    OPERATORS_REVERSE = reverse_dict(OPERATORS_PARSED)

    @classmethod
    def generate_help(cls):
        BLANK = ('\\bullet', '\\bullet', '\\bullet')
        help = {}
        for (k, v) in cls.OPERATORS.items():
            n = cls.OPERATORS_REVERSE[k]
            if v['type'] == 'SUM':
                if v['subtype'] == 'CON':
                    help[n] = {'name': n,
                               'latex': v['latex'] % BLANK,
                               'spelling': n,
                               'example': '%s de un à deux de lambda au carré' % n,
                               'example-latex': v['latex'] % ('1', '2', '\\lambda^2')}
                elif v['subtype'] == 'DIS':
                    help[n] = {'name': n,
                               'latex': v['latex'] % BLANK,
                               'spelling': n,
                               'example': '%s pour lambda égal un à dix de lambda au carré' % n,
                               'example-latex': v['latex'] % ('\\lambda=1', '10', '\\lambda^2')}
            if v['type'] == 'LIM':
                if v['subtype'] == 'LIM':
                    help[n] = {'name': n,
                               'latex': v['latex'] % BLANK,
                               'spelling': n,
                               'example': '%s quand n tend vers l\'infini de u de n' % n,
                               'example-latex': v['latex'] % ('n', '\\infty', 'u_n')}

        return help
