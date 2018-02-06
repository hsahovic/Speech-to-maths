class BigOperatorConstructions:

    OPERATORS = {'ITG': {'latex': '\int_{%s}^{%s} %s', 'priority': 1, 'type': 'SUM'},
                 'SUM': {'latex': '\sum_{%s}^{%s} %s', 'priority': 1, 'type': 'SUM'},
                 'PRO': {'latex': '\prod_{%s}^{%s} %s','priority': 2, 'type': 'SUM'},
                 'ITR': {'latex': '\bigcap_{%s}^{%s} %s','priority': 2, 'type': 'SUM'},
                 'UNI': {'latex': '\bigcup_{%s}^{%s} %s','priority': 1, 'type': 'SUM'}}

    OPERATORS_PARSED = {'intégrale': 'ITG',
                        'somme': 'SUM',
                        'produit': 'PRO',
                        'intersection': 'ITR',
                        'union': 'UNI'}
