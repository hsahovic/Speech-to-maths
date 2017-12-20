#### EN DÉVELOPPEMENT ####
### 


from s2m.core.formulae import Formula
from s2m.core.number import Number
from s2m.core.binop import BigOperator
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

    def __init__(self, o, *args): ##EN CONSTRUCTION !! ## à adapter avec args  
        if o not in self.operators:
            raise ValueError('Unknown big operator code : %r' % o)
        if o in ['INT','SOM','PRO','ITR','UNI']:
            if len(args) > 3 or len(args)==0: raise ValueError('Wrong amout of arguments for operator: %r' % len(args))    
        for form in args: 
            if not isinstance(form, Formula):
                raise ValueError('Input not Formula : %r' % form)
        self.__fl=args
        self.__o=o
            

    def __getattr__(self, p):
        if p == 'o':
            return self.__o
        elif p == 'fl':
            return self.__fl
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
            if other.o == self.__o and len(other.l)==len(self.__fl):
                for i, form in enumerate(self.__fl):
                    if not (form == other.fl[i]): return False
                else: return True
         return False

   

    def _latex(self):
        if self.__o in ['ITG','SOM','PRO','ITR','UNI']:
            c_tex, c_level='',0
            d_tex, d_level='',0
            u_tex, u_level='',0
            if len(self.__fl)==1:
                c_tex, c_level=self.__fl[len(self.__fl)-1].latex()
            if len(self.__fl)==2:
                c_tex, c_level=self.__fl[len(self.__fl)-1].latex()
                d_tex, d_level=self.__fl[0].latex()
            if len(self.__fl)==3:
                c_tex, c_level=self.__fl[len(self.__fl)-1].latex()
                d_tex, d_level=self.__fl[0].latex()
                u_tex, u_level=self.__fl[1].latex()
            return self.latex_model % (d_tex,u_tex,c_tex), c_level
        else: return '',0

    def count_brackets(self):
        return count_brackets(self.___fl(len(self.__fl)-1))
        
    def a_similarity(self, f):
         if isinstance(other, BigOperator) \
           and self.__o == other.o:
           s=0
           for i in range(len(self.__fl)):
               s+=(self.__l(i)).a_similarity
            return s/len(self.__fl)
        else:
            return 0.

    def d_symmetry(self):
        pass
    def teach(self):
        pass

     def latex(self):
        """Genere le code LaTeX correspondant a self"""
        return self._latex()[0]

    def transcription(self):
        pass
      



