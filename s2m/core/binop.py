from s2m.core.formulae import Formula
from s2m.core.number import Number
from s2m.core.utils import reverse_dict


class BinaryOperator(Formula):

    __OPERATORS = {'EQU': {'latex': '%s = %s', 'priority': 0, 'associative': True, 'weak': False, 'nobrackets': True},
                   'NEQ': {'latex': '%s \neq %s', 'priority': 0, 'associative': True, 'weak': False, 'nobrackets': False},
                   'GEQ': {'latex': '%s \geq %s', 'priority': 0, 'associative': True, 'weak': False, 'nobrackets': False},
                   'LEQ': {'latex': '%s \leq %s', 'priority': 0, 'associative': True, 'weak': False, 'nobrackets': False},
                   'EQV': {'latex': '%s \sim %s', 'priority': 0, 'associative': True, 'weak': False, 'nobrackets': False},
                   'SEQ': {'latex': '%s \simeq %s', 'priority': 0, 'associative': True, 'weak': False, 'nobrackets': False},
                   'SBS': {'latex': '%s \subset %s', 'priority': 0, 'associative': True, 'weak': False, 'nobrackets': False},
                   'SPS': {'latex': '%s \supset %s', 'priority': 0, 'associative': True, 'weak': False, 'nobrackets': False},
                   #'INT': {'latex': '\int_{%s}^{%s}', 'priority': 0, 'associative': True, 'weak': False, 'nobrackets': True},
                   #'SUM': {'latex': '\sum_{%s}^{%s}', 'priority': 0, 'associative': True, 'weak': False, 'nobrackets': True},
                   'ADD': {'latex': '%s + %s', 'priority': 1, 'associative': True, 'weak': False, 'nobrackets': False},
                   'SUB': {'latex': '%s - %s', 'priority': 1, 'associative': False, 'weak': True, 'nobrackets': False},
                   'PMS': {'latex': '%s \pm %s', 'priority': 1, 'associative': True, 'weak': True, 'nobrackets': False},
                   'MPS': {'latex': '%s \mp %s', 'priority': 1, 'associative': True, 'weak': True, 'nobrackets': False},
                   'MUL': {'latex': '%s \\times %s', 'priority': 2, 'associative': True, 'weak': False, 'nobrackets': False},
                   'DIV': {'latex': '\\frac{%s}{%s}', 'priority': 2, 'associative': False, 'weak': False, 'nobrackets': True},
                   'CMP': {'latex': '%s \circ %s', 'priority': 2, 'associative': True, 'weak': False, 'nobrackets': False},
                   'VEC': {'latex': '%s \ %s', 'priority': 2, 'associative': True, 'weak': False, 'nobrackets': False},
                   'POW': {'latex': '{%s}^{%s}', 'priority': 3, 'associative': False, 'weak': False, 'nobrackets': False},
                   'EVL': {'latex': '%s \\left( %s \\right)', 'priority': 4, 'associative': False, 'weak': False, 'nobrackets': True},
                   }

    __OPERATORS_PARSED = {'plus': 'ADD',
                          'moins': 'SUB',
                          'fois': 'MUL',
                          'sur': 'DIV',
                          'puissance': 'POW',
                          'égal': 'EQU',
                          'différent de': 'NEQ',
                          'supérieur à': 'GEQ',
                          'inférieur à': 'LEQ',
                          'plus ou moins': 'PSM',
                          'moins ou plus': 'MPS',
                          'rond': 'CMP',
                          'vectoriel': 'VEC',
                          'inclus dans': 'SBS',
                          'contient': 'SPS',
                          'équivaut à': 'EQV',
                          'environ égal à': 'SEQ',
                          'intégrale': 'INT',
                          'somme': 'SUM',
                          'de': 'EVL',
                          }

    __OPERATORS_REVERSE = reverse_dict(__OPERATORS_PARSED)

    def __init__(self, l, o, r):

        if o not in self.operators:
            raise ValueError('Unknown binary operator code : %r' % o)
        elif not issubclass(l.__class__, Formula):
            raise TypeError(
                'LHS of binary operator must be a well-formed formula')
        elif not issubclass(r.__class__, Formula):
            raise TypeError(
                'RHS of binary operator must be a well-formed formula')
        else:
            self.__l, self.__o, self.__r = l, o, r

    def __getattr__(self, p):

        if p == 'l':
            return self.__l
        elif p == 'o':
            return self.__o
        elif p == 'r':
            return self.__r
        elif p == 'priority':
            return self.__OPERATORS[self.__o]['priority']
        elif p == 'associative':
            return self.__OPERATORS[self.__o]['associative']
        elif p == 'latex_model':
            return self.__OPERATORS[self.__o]['latex']
        elif p == 'weak':
            return self.__OPERATORS[self.__o]['weak']
        elif p == 'nobrackets':
            return self.__OPERATORS[self.__o]['nobrackets']
        elif p == 'operators':
            return self.__OPERATORS.keys()
        else:
            raise AttributeError

    def __eq__(self, other):
	
        if other and isinstance(other, BinaryOperator):
            return other.l == self.__l and other.o == self.__o and other.r == self.__r
        return False

    def __hash__(self):

        return hash(self.__l) ^ hash(self.__o) ^ hash(self.__r)

    def count_brackets(self):
        """Donne le nombre de blocs parentheses et le nombre de blocs non
           parentheses dans le code LaTeX genere"""

        y, n = 0, 0

        if self.__l.priority < self.priority \
           and not self.nobrackets:
            n += 1
        else:
            y += 1

        l_brackets = self.__l.count_brackets()
        y += l_brackets[0]
        n += l_brackets[1]

        if self.__r.priority < self.priority \
           and not self.nobrackets:
            n += 1
        else:
            y += 1

        r_brackets = self.__r.count_brackets()
        y += r_brackets[0]
        n += r_brackets[1]

        return y, n

    def distance(self, f):
        """Definit une (pseudo-)distance entre self et une autre formule f"""

        if f.__class__ == BinaryOperator:
            if f.o == self.__o:
                return 0.4 * (self.__l.distance(f.l) + self.__r.distance(f.r))
            else:
                return 1.
        elif issubclass(f.__class__, Formula):
            return 1.
        else:
            raise TypeError('Cannot compare formula with non-formula %r' % f)

    def flatten(self):
        """Liste les enfants de self dans la representation n-aire minimale"""

        children = []

        if self.__l.__class__ == BinaryOperator \
           and self.__l.priority == self.priority:
            children.extend(self.__l.flatten())
        else:
            children.append(self.__l)

        if self.__r.__class__ == BinaryOperator \
           and self.__r.priority == self.priority:
            children.extend(self.__r.flatten())
        else:
            children.append(self.__r)

        return children

    def symmetry_index(self):
        """Evalue la symetrie de self"""

        if not self.associative:
            return 1 - min(self.__l.distance(self.__r),
                           1 - 0.25 * self.__l.symmetry_index()
                             - 0.25 * self.__r.symmetry_index())
        else:
            children = self.flatten()
            l = len(children)
            chart = [[0. for _ in range(l)]
                     for __ in range(l)]
            s = 0
            for i in range(l):
                for j in range(i + 1, l):
                    chart[i][j] = children[i].distance(children[j])
                co_child_sym = 1 - 0.5 * children[i].symmetry_index()
                sum_dist = (sum(chart[i]) + sum(chart[k][i]
                                                for k in range(0, i))) / (l - 1)
                s += min(co_child_sym, sum_dist)
            return 1 - s / l

    def _latex(self):

        if self.__l.priority < self.priority \
           and not self.nobrackets:
            l_content, l_level = self.__l._latex()
            l_level += 1
            l_tex = self.brackets_model(l_level) % l_content
        else:
            l_tex, l_level = self.__l._latex()

        if (self.__r.priority < self.priority
                or (self.__r.priority == self.priority and self.weak)) \
                and not self.nobrackets:
            r_content, r_level = self.__r._latex()
            r_level += 1
            r_tex = self.brackets_model(r_level) % r_content
        else:
            r_tex, r_level = self.__r._latex()

        return self.latex_model % (l_tex, r_tex), max(l_level, r_level)

    def latex(self):
        """Genere le code LaTeX correspondant a self"""
        return self._latex()[0]

    def transcription(self):

        if self.__o == 'POW' \
           and self.__r.__class__ == Number \
           and self.__r.val == 2:
            return self.__l.transcription() + ' au carré'
        else:
            return '%s %s %s' % (self.__l.transcription(),
                                 self.__OPERATORS_REVERSE[self.__o],
                                 self.__r.transcription())

    def teach(parser):

        binary_operator_easy = ('binaryoperator-operator',
                                BinaryOperator.__OPERATORS_PARSED,
                                lambda x: x)

        # Defines A op B -> BinaryOperator(A, op, B)
        def binary_operator_complex_expand(formulae):
            return BinaryOperator(formulae[0], formulae[1], formulae[2])

        binary_operator_complex = ('binaryoperator',
                                   '%f $binaryoperator-operator %f',
                                   binary_operator_complex_expand,
                                   True)

        # Defines A carre -> BinaryOperator(A, 'POW', Number(2))
        def squared_complex_expand(formulae):
            return BinaryOperator(formulae[0], 'POW', Number(2))

        squared_complex = ('squared',
                           '%f au carré',
                           squared_complex_expand,
                           True)

        parser.add_easy_reduce(*binary_operator_easy)
        parser.add_complex_rule(*binary_operator_complex)
        parser.add_complex_rule(*squared_complex)
