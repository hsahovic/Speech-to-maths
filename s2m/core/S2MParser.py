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

        #pas de tests sur le type
        parses = self.__parser.cky(w)
        if formal:
            return parses
        else:
            return listset([(p.latex(), p.evaluation()) for p in parses])

    def __call__(self, w, formal=False):
        return self.parse(w, formal=formal)

s2m_parser = S2MParser()
