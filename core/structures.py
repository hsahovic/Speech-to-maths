"""[PSC Speech-to-Math]             (Streichholzschaechtelchen)
                       structures.py
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

from abc import ABCMeta, abstractmethod

class Formula:
    __metaclass__ = ABCMeta
    @abstractmethod
    def priority(self):
        pass
    @abstractmethod
    def latex(self, level=0):
        pass

def brackets(level):
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
    __operators = {'ADD': {'latex': '%s + %s', 'priority': 1},
                   'SUB': {'latex': '%s - %s', 'priority': 1},
                   'MUL': {'latex': '%s \\times %s', 'priority': 2},
                   'DIV': {'latex': '\\frac{%s}{%s}', 'priority': 2},
                   'POW': {'latex': '{%s}^{%s}', 'priority': 3},
                   'EQU': {'latex': '%s = %s', 'priority': 5}}
    __l, __o, __r = None, None, None
    def __init__(self, l, o, r):
        if o not in self.__operators.keys():
            raise ValueError('Unknown binary operator code : %r' % o)
        elif not issubclass(l.__class__, Formula):
            raise TypeError('LHS of binary operator must be a well-formed formula')
        elif not issubclass(r.__class__, Formula):
            raise TypeError('RHS of binary operator must be a well-formed formula')
        else:
            self.__l, self.__o, self.__r = l, o, r
    def get_l(self):
        return self.__l
    def get_o(self):
        return self.__o
    def get_r(self):
        return self.__r
    def priority(self):
        return self.__operators[self.__o]['priority']
    def latex(self, level=0):
        if self.__l.priority() < self.priority():
            l_tex = brackets(level+1) % self.__l.latex(level+1)
        else:
            l_tex = self.__l.latex(level)
        if self.__r.priority() < self.priority():
            r_tex = brackets(level+1) % self.__r.latex(level+1)
        else:
            r_tex = self.__r.latex(level)
        return self.__operators[self.__o]['latex'] % (l_tex, r_tex)

class UnaryOperator(Formula):
    __operators = {'NEG': {'latex':'-%s', 'priority': 4},
                   'SQR': {'latex':'\sqrt{%s}', 'priority': 5}}
    __o, __r = None, None
    def __init__(self, o, r):
        if o not in self.__operators.keys():
            raise ValueError('Unknown unary operator code : %r' % o)
        elif not issubclass(r.__class__, Formula):
            raise TypeError('Operand of unary operator must be a well-formed formula') 
        else:
            self.__o, self.__r = o, r
    def get_o(self):
        return self.__o
    def get_r(self):
        return self.__r
    def priority(self):
        return self.__operators[self.__o]['priority']
    def latex(self, level=0):
        if self.__r.priority() < self.priority():
            r_tex = brackets(level+1) % self.__r.latex(level+1)
        else:
            r_tex = self.__r.latex(level)
        return self.__operators[self.__o]['latex'] % r_tex        

class Variable(Formula):
    __v = None
    def __init__(self, v):
        if type(v) is not str:
            raise TypeError('Variable identifier must be a string, not %r' % v)
        else:
            self.__v = v
    def get_v(self):
        return self.__v
    def priority(self):
        return 5
    def latex(self, level=0):
        return self.__v

class Number(Formula):
    __n = None
    def __init__(self, n):
        if type(n) is not float \
           and type(n) is not int:
            raise TypeError('Number must be a float or an int, not %r' % n)
        else:
            self.__n = n
    def get_n(self):
        return self.__n
    def priority(self):
        return 5
    def latex(self, level=0):
        return repr(self.__n)
