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

class Formula:
    
    __metaclass__ = ABCMeta

    @abstractmethod
    def latex(self, level=0):
        pass

    @abstractmethod
    def count_brackets(self):
        pass

    @abstractmethod
    def natural_bracketting_index(self):
        pass

    @abstractmethod
    def distance(self, f):
        pass

    @abstractmethod
    def symmetry_index(self):
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

    __OPERATORS = {'ADD': {'latex': '%s + %s', 'priority': 1, 'associative': True, 'weak': False},
                   'SUB': {'latex': '%s - %s', 'priority': 1, 'associative': False, 'weak': True},
                   'MUL': {'latex': '%s \\times %s', 'priority': 2, 'associative': True, 'weak': False},
                   'DIV': {'latex': '\\frac{%s}{%s}', 'priority': 2, 'associative': False, 'weak': False},
                   'POW': {'latex': '{%s}^{%s}', 'priority': 3, 'associative': False, 'weak': False},
                   'EQU': {'latex': '%s = %s', 'priority': 0, 'associative': True, 'weak': False}}

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
        elif p == 'operators':
            return self.__OPERATORS.keys()
        else:
            raise AttributeError

    def count_brackets(self):
        """Donne le nombre de blocs parentheses et le nombre de blocs non
           parentheses dans le code LaTeX genere"""
        
        y, n = 0, 0

        if self.__l.priority < self.priority:
            n += 1
        else:
            y += 1

        l_brackets = self.__l.count_brackets()
        y += l_brackets[0]
        n += l_brackets[1]
            
        if self.__r.priority < self.priority:
            n += 1
        else:
            y += 1

        r_brackets = self.__r.count_brackets()
        y += r_brackets[0]
        n += r_brackets[1]

        return y, n

    def natural_bracketting_index(self):
        """Donne la proportion de blocs parentheses dans le code LaTeX
           parmi l'ensemble des blocs generes"""

        brackets = self.count_brackets()
        return float(brackets[0]) / (brackets[0] + brackets[1])

    #SYmmetry Distance
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

    #Flatten
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

    #SYmmetry Index
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
    
    def latex(self, level=0):
        """Genere le code LaTeX correspondant a self"""

        if self.__l.priority < self.priority:
            l_tex = self.brackets_model(level+1) % self.__l.latex(level+1)
        else:
            l_tex = self.__l.latex(level)

        if self.__r.priority < self.priority \
           or (self.__r.priority == self.priority and self.weak):
            r_tex = self.brackets_model(level+1) % self.__r.latex(level+1)
        else:
            r_tex = self.__r.latex(level)

        return self.latex_model % (l_tex, r_tex)

    
class UnaryOperator(Formula):

    __OPERATORS = {'NEG': {'latex':'-%s', 'priority': 4},
                   'SQR': {'latex':'\sqrt{%s}', 'priority': 5}}

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
        elif p == 'operators':
            return self.__OPERATORS.keys()
        else:
            raise AttributeError

    def count_brackets(self):

        y, n = 0, 0

        if self.__r.priority < self.priority:
            n += 1
        else:
            y += 1

        r_brackets = self.__r.count_brackets()
        y += r_brackets[0]
        n += r_brackets[1]

        return y, n

    def natural_bracketting_index(self):

        brackets = self.count_brackets()
        return float(brackets[0]) / (brackets[0] + brackets[1])

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

    def latex(self, level=0):

        if self.__r.priority < self.priority:
            r_tex = self.brackets_model(level+1) % self.__r.latex(level+1)
        else:
            r_tex = self.__r.latex(level)

        return self.latex_model % r_tex        

    
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

    def natural_bracketting_index(self):

        return 1.

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
        
    def latex(self, level=0):

        return self.__v

    
class Number(Formula):

    def __init__(self, n):

        if type(n) is not float \
           and type(n) is not int:
            raise TypeError('Number must be a float or an int, not %r' % n)
        else:
            self.__n = n

    def __getattr__(self, p):

        if p == 'n':
            return self.__n
        elif p == 'priority':
            return 5
        else:
            raise AttributeError

    def count_brackets(self):

        return 0, 0

    def natural_bracketting_index(self):

        return 1.

    def distance(self, f):

        if f.__class__ == Number:
            if f.n == self.__n:
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
        
    def latex(self, level=0):

        return repr(self.__n)
