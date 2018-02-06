class UnaryOperatorConstructions:

    OPERATORS = {'NEG': {'latex': '-%s', 'priority': 4, 'nobrackets': False},
                 'SQR': {'latex': '\\sqrt{%s}', 'priority': 5, 'nobrackets': True},
                 '3SQ': {'latex': '\\sqrt[3]{%s}', 'priority': 5, 'nobrackets': True},
                 'ABS': {'latex': '\\left| %s \\right|', 'priority': 5, 'nobrackets': True}
    }

    OPERATORS_PARSED = {'moins': 'NEG',
                        'racine de': 'SQR',
                        'racine carré de': 'SQR',
                        'racine cubique de': '3SQ',
                        'valeur absolu de': 'ABS'
    }
