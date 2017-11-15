from s2m.core.parser import Parser
from s2m.core.formulae import Formula
from s2m.core.binop import BinaryOperator
from s2m.core.unop import UnaryOperator
from s2m.core.bracketted_block import BrackettedBlock
from s2m.core.variable import Variable
from s2m.core.number import Number
from s2m.core.utils import listset
from s2m.core.sphinx_config import SphinxConfig

import random

class S2MParser():

    def __init__(self):
        self.__parser = Parser()
        Variable.teach(self.__parser)
        Number.teach(self.__parser)
        BinaryOperator.teach(self.__parser)
        UnaryOperator.teach(self.__parser)
        BrackettedBlock.teach(self.__parser)
        self.__parser.sphinx_config.update_config_files()

    def parse(self, w, formal=False):
        fitf = lambda x: 0.5*x.natural_bracketting_index()+0.1*x.symmetry_index()
        #Stupid
        #Modifier le format de token pour séparer formula de data
        if type(w) == str:
            parses = self.__parser.cky(w)
        elif type(w) == list:
            parses = []
            for x in w:
                parses.extend(set(self.__parser.cky(x)))
        else:
            raise TypeError
        if formal:
            return parses
        else:
            return listset([p.latex() for p in sorted(parses, key=fitf, reverse=True)])

    def __call__(self, w, formal=False):
        return self.parse(w, formal=formal)

s2m_parser = S2MParser()
