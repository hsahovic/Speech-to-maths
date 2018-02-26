"""[PSC Speech-to-Math]                                 (loift)
                        3trees.py
***************************************************************
*       Extrait d'un arbre synthaxique                        *
*       tous ses sous-arbres de profondeur égale à trois,     *
*       avec leur fréquence dans l'arbre considéré.           *
************************************************************"""

from s2m.core.formulae import Formula
from s2m.core.number import Number 
from s2m.core.number import Variable
from s2m.core.unop import UnaryOperator
from s2m.core.binop import BinaryOperator
from s2m.core.bigop import BigOperator




class ThreeTrees: 
    def __init__(self):
       self.__3trees={} "arbres en clefs, occurences en valeurs"

    def __getattr__(self,p):
        if(p=='t'):
            return self.__3trees
        else:
            "..
            "

    def add3tree(self,tree):
        "tree est de profondeur 3"
        if(tree in self.__3trees.keys()):
            self.__3trees[tree]+=1
        else :
            self.__3trees.add(tree,1)
    
    def isa3tree(self,tree)
        "dit si un arbre est un 3tree ou non"

    def extract3trees(self,formula):
        if(isinstance(formula,Number):
            return 1
        if(isinstance(formula,Variable):
            return 1
        if(isinstance(formula,UnaryOperator)):
            h = max(self.extract3trees(formula.r) + 1 
            if h ==3:
                " rajouter aux 3 arbres "

        if(isinstance(formula,BinaryOperator)):
           
        

        "cœur de la classe"