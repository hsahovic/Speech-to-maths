#### EN DÉVELOPPEMENT ####
### 


from s2m.core.formulae import Formula
from s2m.core.number import Number
from s2m.core.utils import reverse_dict

import random


class BigOperator(Formula):

# Est-ce qu'on gère le contenu du BigOp ? Normalement oui ! 
    __OPERATORS = {'ITG': {'latex': '\int_{%s}^{%s} %s', 'priority': 1},
    'SOM': {'latex': '\sum_{%s}^{%s} %s', 'priority': 1},
    'PRO': {'latex': '\prod_{%s}^{%s} %s','priority': 2},
    'ITR': {'latex': '\prod_{%s}^{%s} %s','priority': 2},
    'UNI': {'latex': '\prod_{%s}^{%s} %s','priority': 1}}

    __OPERATORS_PARSED = {'intégrale': 'ITG',
     'somme': 'SOM',
     'produit': 'PRO',
     'intersection': 'ITR',
      'union': 'UNI'}

    __OPERATORS_REVERSE = reverse_dict(__OPERATORS_PARSED)

    def __init__(self, *args): ##EN CONSTRUCTION !! ## à adapter avec args  
        l=[]
        i=0
        for a in args:
            i+=1
            if a in self.operators

    ## à réécrire
        if len(l)=0 or len(l)>3 :
             raise ValueError('Bad attributes list')
        if l[0] not in self.operators:
            raise ValueError('Unknown binary operator code : %r' % o)
        self.__o = l[Ø]
        if len(l)==1:
            self.__d=None #down
            self.__u=None #up
            self.__c=None #content
        else if len(l)==2:
            self.__d,self.__u,self.__c=l[1],None,None
        else if len(l)==3:
            self.__d,self.__u,self.__c=l[1],l[2],None
        else if len(l)==4:
             self.__d,self.__u,self.__c=l[1],l[2],l[3)
        self.__size=len(l)-1
        
        
    def __getattr__(self, p):
        elif p == 'o':
            return self.__o
        elif p == 'd':
            if self__d is None :
                raise AttributeError
            else :
                return self.__d
        elif p == 'u':
            if self__u is None :
                raise AttributeError
            else :
                return self.__u
        elif p == 'c':
            if self__c is None :
                raise AttributeError
            else :
                return self.__c
        elif p == 'size':
            return self.__size
        elif p == 'priority':
            return self.__OPERATORS[self.__o]['priority']
        elif p == 'latex_model':
            return self.__OPERATORS[self.__o]['latex']
        elif p == 'operators':
            return self.__OPERATORS.keys()
        else:
            raise AttributeError

    def __eq__(self, other):
         if other and isinstance(other, BigOperator):
            if other.o == self.__o:
                    return other.u == self.__u and other.d == self.__d and other_c == self.__c
        return False

   

    def _latex(self):

    
    def latex(self):
        """Genere le code LaTeX correspondant a self"""
        return self._latex()[0]

    def transcription(self):

      



