#Temp
from s2m.core.parser_n2 import Parser
#End-Temp
from s2m.core.formulae import Formula
from s2m.core.binop import BinaryOperator
from s2m.core.unop import UnaryOperator
from s2m.core.bracketted_block import BrackettedBlock
from s2m.core.variable import Variable
from s2m.core.number import Number
from s2m.core.bigop import BigOperator
from s2m.core.placeholder import PlaceHolder
from s2m.core.utils import listset
from s2m.core.utils import normalize_scores
from s2m.core.sphinx_config import SphinxConfig
from s2m.core.proximity_dict import ProximityDict
from s2m.core.s2m_training import s2m_training

from s2m.core.S2MParser_utils import append_formulae

import random

class S2MParser():

    def __init__(self):
        self.__proximity_dict = ProximityDict()
        self.__proximity_dict.load('s2m/core/sphinx/s2m.dict',
                                   map='s2m/core/sphinx/fr.map')
        self.__parser = Parser(self.__proximity_dict,
                               PlaceHolder=PlaceHolder)
        Variable.teach(self.__parser)
        Number.teach(self.__parser)
        BinaryOperator.teach(self.__parser)
        UnaryOperator.teach(self.__parser)
        BrackettedBlock.teach(self.__parser)
        BigOperator.teach(self.__parser)
        PlaceHolder.teach(self.__parser)
        self.__parser.sphinx_config.update_config_files()
        #décommenter ceci après dev
        #s2m_training.enable_system_training()

    def help(self, s):
        return self.__parser.help_dict.get_all(s)
             
    def parse(self, w, sess, document, formal=False, save=True, **args):

        parses = self.__parser.myers(w, sess, document, **args)
        if formal:
            return parses
        else:
            results = normalize_scores(listset(sorted(
                [(p[0][0].latex(), p[0][0].evaluation(sess, document)) for p in parses
                if isinstance(p[0][0], Formula)], key=lambda x: x[1], reverse=True)))
            filtered_parses = [p for p in parses if isinstance(p[0][0], Formula)]
            if save:
                token = append_formulae(filtered_parses, document)
                return results, token
            else:
                return results

    def __call__(self, w, sess, document, **args):
        return self.parse(w, sess, document, **args)

s2m_parser = S2MParser()
