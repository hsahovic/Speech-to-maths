"""[PSC Speech-to-Math]             (Streichholzschaechtelchen)
                        formulae.py
***************************************************************
*Fournit les structures de base pour l'encodage des arbres    *
*syntaxiques, descendantes de la classe abstraite Formula.    *
*La conversion d'un bloc en code LaTeX est obtenue par appel a*
*la fonction membre latex.                                    * 
*La priorite des operations est prise en compte et le paren-  *
*thesage est ajuste automatiquement en consequence.           *
*Les attributs debutant par un double <i>underscore</i> sont  *
*prives.                                                      *
************************************************************"""

#BEWARE: THIS IS PYTHON 2 METACLASS SYNTAX

#Niveaux de priorite a gerer proprement... comment ?

from abc import ABCMeta, abstractmethod
from number_parser import NumberParser
from parser import Token

class Formula:
    
    __metaclass__ = ABCMeta

    @abstractmethod
    def _latex(self):
        pass
               
    @abstractmethod
    def latex(self):
        pass

    @abstractmethod
    def count_brackets(self):
        pass

    def natural_bracketting_index(self):
        """Donne la proportion de blocs parentheses dans le code LaTeX
           parmi l'ensemble des blocs generes"""

        brackets = self.count_brackets()
        if brackets[0] == brackets[1] == 0:
            return 1.
        else:
            return float(brackets[0]) / (brackets[0] + brackets[1])

    @abstractmethod
    def distance(self, f):
        pass

    @abstractmethod
    def symmetry_index(self):
        pass

    @abstractmethod
    def parsing_rules():
        pass

    def brackets_model(self, level):

        if type(level) is not int:
            raise TypeError('Bracket level must be an int, not %r' % i)
        elif level < 1:
            raise ValueError('Bracket level must be non-negative, not %r' % i)
        elif 0 < level < 4:
            return '\\left( %s \\right)'
        elif 4 < level < 6:
            return '\\left[ %s \\right]'
        elif level > 6:
            return '\\left\\lbrace %s \\right\\rbrace'

    
class BinaryOperator(Formula):

    __OPERATORS = {'ADD': {'latex': '%s + %s', 'priority': 1, 'associative': True, 'weak': False, 'nobrackets': False},
                   'SUB': {'latex': '%s - %s', 'priority': 1, 'associative': False, 'weak': True, 'nobrackets': False},
                   'MUL': {'latex': '%s \\times %s', 'priority': 2, 'associative': True, 'weak': False, 'nobrackets': False},
                   'DIV': {'latex': '\\frac{%s}{%s}', 'priority': 2, 'associative': False, 'weak': False, 'nobrackets': True},
                   'POW': {'latex': '{%s}^{%s}', 'priority': 3, 'associative': False, 'weak': False, 'nobrackets': False},
                   'EQU': {'latex': '%s = %s', 'priority': 0, 'associative': True, 'weak': False, 'nobrackets': True}}

    def __init__(self, l, o, r):

        if o not in self.operators:
            raise ValueError('Unknown binary operator code : %r' % o)
        elif not issubclass(l.__class__, Formula):
            raise TypeError('LHS of binary operator must be a well-formed formula')
        elif not issubclass(r.__class__, Formula):
            raise TypeError('RHS of binary operator must be a well-formed formula')
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
            chart = [ [ 0. for _ in range(l) ]
                      for __ in range(l) ]
            s = 0
            for i in range(l):
                for j in range(i+1, l):
                    chart[i][j] = children[i].distance(children[j])
                co_child_sym = 1 - 0.5 * children[i].symmetry_index()
                sum_dist = (sum(chart[i]) + sum(chart[k][i] for k in range(0, i))) / (l - 1)
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

        if (self.__r.priority < self.priority \
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

    def parsing_rules():

        def binary_operator_reduce(word):
            OPERATORS = {'plus':'ADD',
                         'moins':'SUB',
                         'fois':'MUL',
                         'sur':'DIV',
                         'puissance':'POW',
                         'egal':'EQU'}
            if word in OPERATORS.keys():
                return Token('binaryoperator-operator', [OPERATORS[word]])
            else:
                return None

        #Defines A op B -> BinaryOperator(A, op, B)
        def binary_operator_complex_expand(words):
            return BinaryOperator(words[0], words[1], words[2])

        binary_operator_complex = ('binaryoperator',
                                   '%f $binaryoperator-operator %f',
                                   binary_operator_complex_expand)

        #Definales A carre -> BinaryOperator(A, 'POW', Number(2))
        def squared_complex_expand(words):
            return BinaryOperator(words[0], 'POW', Number(2))

        squared_complex = ('squared',
                           '%f au carre',
                           squared_complex_expand)
        
        return [], \
               [binary_operator_reduce], \
               [], \
               [binary_operator_complex, squared_complex]

    
class UnaryOperator(Formula):

    __OPERATORS = {'NEG': {'latex':'-%s', 'priority': 4, 'nobrackets': False},
                   'SQR': {'latex':'\sqrt{%s}', 'priority': 5, 'nobrackets': True}}

    def __init__(self, o, r):

        if o not in self.operators:
            raise ValueError('Unknown unary operator code : %r' % o)
        elif not issubclass(r.__class__, Formula):
            raise TypeError('Operand of unary operator must be a well-formed formula') 
        else:
            self.__o, self.__r = o, r

    def __getattr__(self, p):

        if p == 'o':
            return self.__o
        elif p == 'r':
            return self.__r
        elif p == 'priority':
            return self.__OPERATORS[self.__o]['priority']
        elif p == 'latex_model':
            return self.__OPERATORS[self.__o]['latex']
        elif p == 'nobrackets':
            return self.__OPERATORS[self.__o]['nobrackets']
        elif p == 'operators':
            return self.__OPERATORS.keys()
        else:
            raise AttributeError

    def count_brackets(self):

        y, n = 0, 0

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

        if f.__class__ == UnaryOperator:
            if f.o == self.__o:
                return self.__r.distance(f.r)
            else:
                return 1.
        elif issubclass(f.__class__, Formula):
            return 1.
        else:
            raise TypeError('Cannot compare formula with non-formula %r' % f)

    def symmetry_index(self):

        return self.__r.syi()

    def _latex(self):

        if self.__r.priority < self.priority \
           and not self.nobrackets:
            r_content, r_level = self.__r._latex()
            r_level += 1
            r_tex = self.brackets_model(r_level) % r_content
        else:
            r_tex, r_level = self.__r._latex()

        return self.latex_model % r_tex, r_level

    def latex(self):

        return self._latex()[0]

    def parsing_rules():

        def unary_operator_reduce(word):
            OPERATORS = {'moins':'NEG'}
            if word in OPERATORS.keys():
                return Token('unaryoperator-operator', [OPERATORS[word]])
            else:
                return None

        #Defines op A -> UnaryOperator(op, A)
        def unary_operator_complex_expand(words):
            return UnaryOperator(words[0], words[1])

        unary_operator_complex = ('unaryoperator',
                                  '$unaryoperator-operator %f',
                                  unary_operator_complex_expand)

        #Defines racine de A -> UnaryOperator('SQR', A)
        def sqr_complex_expand(words):
            return UnaryOperator('SQR', words[0])

        sqr_complex = ('sqr-unaryoperator',
                       'racine de %f',
                       sqr_complex_expand)

        return [], \
               [unary_operator_reduce], \
               [], \
               [unary_operator_complex, sqr_complex]

    
class BrackettedBlock(Formula):

    def __init__(self, b):

        if not issubclass(b.__class__, Formula):
            raise TypeError('Operand of bracketted block must be a well-formed formula')
        else:
            self.__b = b

    def __getattr__(self, p):
        
        if p == 'b':
            return self.__b
        elif p == 'priority':
            return 5
        else:
            raise AttributeError

    def _latex(self):

        b_tex, b_level = self.__b._latex()
        return self.brackets_model(b_level+1) % b_tex, b_level+1
        
    def latex(self):

        return self._latex()[0]
        
    def count_brackets(self):

        y, n = self.__b.count_brackets()
        return y + 1, n

    def distance(self, f):

        return self.__b.distance(f)

    def symmetry_index(self):

        return self.__b.symmetry_index()

    def parsing_rules():

        def bracketted_block_complex_expand(words):
            return BrackettedBlock(words[0])

        bracketted_block_explicit_complex = ('brackettedblock-explicit',
                                             'ouvrez la parenthese %f fermez la parenthese',
                                             bracketted_block_complex_expand)

        bracketted_block_implicit_complex = ('brackettedblock-implicit',
                                             'entre parentheses %f',
                                             bracketted_block_complex_expand)

        return [], [], [], [bracketted_block_explicit_complex, \
                            bracketted_block_implicit_complex]

    
class Variable(Formula):

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

    def parsing_rules():

        def variable_radio_roman_reduce(word):
            RADIO_ROMAN = ['alpha', 'bravo', 'charlie', 'delta', 'echo',
                           'uniform', 'xray', 'yankee', 'zulu']
            if word in RADIO_ROMAN:
                return Token('variable', [Variable(word[0])])
            else:
                return None

        return [], [variable_radio_roman_reduce], [], []
    
    
class Number(Formula):

    def __init__(self, n):

        if type(n) == float \
           or type(n) == int \
           or type(n) == str:
            self.__n = n
        else:
            raise TypeError('Number must be a float, an int or a string, not %r' % n)
        
    def __getattr__(self, p):

        if p == 'n':
            return self.__n
        elif p == 'priority':
            return 5
        elif p == 'val':
            if type(self.__n) == str:
                np = NumberParser()
                return np(self.__n)
            else:
                return self.__n
        else:
            raise AttributeError

    def count_brackets(self):

        return 0, 0

    def distance(self, f):

        if f.__class__ == Number:
            if f.val == self.val:
                return 0.
            else:
                return 0.1
        elif f.__class__ == Variable:
            return 0.5
        elif issubclass(f.__class__, Formula):
            return 1.
        else:
            raise TypeError('Cannot compare Number to non-formula %r' % f)

    def symmetry_index(self):

        return 1.

    def _latex(self):

        return repr(self.val), 0
        
    def latex(self):

        return repr(self.val)

    def concat(self, p):

        if type(self.__n) == str \
           and p.__class__ == Number \
           and type(p.n) == str:
            return Number(self.__n + " " + p.n)
        else:
            raise TypeError('Concatenation of Numbers must be applied to Number classes ' \
                            + 'with string-encoded attributes.')

    def parsing_rules():

        def number_reduce(word):
            if word in NumberParser.NUMBER_WORDS:
                return Token('number', [Number(word)])
            else:
                return None

        def number_expand(tok1, tok2, aux):
            if tok1.tag == tok2.tag == 'number':
                return Token('number', [tok1.formula[0].concat(tok2.formula[0])])
            else:
                return None

        return [number_expand], [number_reduce], [], []

    
