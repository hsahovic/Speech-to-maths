"""[PSC Speech-to-Math]           (Streichholzschaechtelchen)
                        parser.py
*************************************************************
*Effectue l'analyse syntaxique d'un texte en francais en    *
*s'appuyant sur les structures definies dans formulae.py.   *
*L'algorithme d'analyse syntaxique employe est CKY.         *
*L'analyseur syntaxique embarque une instance de la classe  *
*de configuration SphinxConfig.                             *
*Le fichier parser_lambdas.py contient les lambdas-fonctions*
*necessaires a la conversion CNF faible -> CNF.             *
*La classe Parser est encapsulee par S2MParser et ne doit   *
*pas etre appelee ou instanciee directement.                *
**********************************************************"""

from s2m.core.sphinx_config import SphinxConfig
from s2m.core.version import *
from s2m.core.utils import _unslash

from functools import reduce
#Priority queue implementation by Daniel Stutzbach
from heapdict import heapdict

#temp
from time import time

class Parser:

    ##Temp
    def temptemp(self):
        return self.__expands, self.__reduces
    ##End-Temp

    def __init__(self, proximity_dict):

        self.__expands = {}
        self.__reduces = {}
        self.__aux = {}
        self.__rule_names = []
        self.__descriptors = {'%f'}
        self.__expression_descriptors = set()
        self.__sphinx_config = SphinxConfig(S2M_GRAMMAR_NAME,
                                            S2M_GRAMMAR_VERSION,
                                            S2M_VERSION)
        self.__proximity_dict = proximity_dict

    def __getattr__(self, p):

        if p == 'sphinx_config':
            return self.__sphinx_config
        elif p == 'proximity_dict':
            return self.__proximity_dict
        else:
            raise AttributeError
        
    def add_expand(self, desc, l_desc, r_desc, f=None):

        lr_desc = (l_desc, r_desc)
        unslashed_desc = _unslash(desc)
        if unslashed_desc in self.__expands:
            self.__expands[unslashed_desc].append((lr_desc, f))
        else:
            self.__expands[unslashed_desc] = [(lr_desc, f)]
            self.__descriptors.add(unslashed_desc)

    def add_reduce(self, desc, word, formula=None):

        unslashed_desc = _unslash(desc)
        if unslashed_desc in self.__reduces:
            self.__reduces[unslashed_desc].append((word, formula))
        else:
            self.__reduces[unslashed_desc] = [(word, formula)]
            self.__descriptors.add(unslashed_desc)

    def _validate_name(self, name, is_expression):

        if name in self.__rule_names:
            raise ValueError('Name %r is already the name of a rule.' % name)
        else:
            self.__rule_names.append(name)
        if is_expression:
            self.__expression_descriptors.add(_unslash('$' + name))

    def add_easy_reduce(self, name, d, f, is_expression=False):

        import s2m.core.parser_lambdas as parser_lambdas

        self._validate_name(name, is_expression)

        unslashed_name = _unslash('$' + name)
        
        k = 0

        for key, val in d.items():
            words = key.split(' ')
            if len(words) == 0:
                raise ValueError('String to be recognized by the parser must be non-empty.')
            elif len(words) == 1:
                self.add_reduce(unslashed_name, key, f(val))
            elif len(words) == 2:
                self.add_reduce('$%s/%r.0' % (name, k), words[0])
                self.add_reduce('$%s/%r.1' % (name, k), words[1])
                self.add_expand(unslashed_name,
                                '$%s/%r.0' % (name, k),
                                '$%s/%r.1' % (name, k),
                                lambda _,val=val: f(val))
                k += 1
            else:
                for i, word in enumerate(words):
                    self.add_reduce('$%s/%r.%r' % (name, k, i), words[i])
                self.add_expand('$%s/%r.0t1' % (name, k),
                                '$%s/%r.0' % (name, k),
                                '$%s/%r.1' % (name, k))
                for i in range(2, len(words)-1):
                    self.add_expand('$%s/%r.0t%r' % (name, k, i),
                                    '$%s/%r.0t%r' % (name, k, i-1),
                                    '$%s/%r.%r' % (name, k, i))
                self.add_expand(unslashed_name,
                                '$%s/%r.0t%r' % (name, k, len(words)-2),
                                '$%s/%r.%r' % (name, k, len(words)-1),
                                lambda _,val=val: f(val))
                k += 1

        self.__sphinx_config.add_simple_rule(name, d.keys(), is_expression)

    def add_complex_rule(self, name, s, f, is_expression=True):

        self._validate_name(name, is_expression)

        unslashed_name = _unslash('$' + name)
        
        words = s.split(' ')
        if len(words) < 2:
            raise ValueError('String describing a complex rule must be composed of at least two words, unlike %r.' % s)        
        is_word = [True] * len(words)
        descs = []
        
        for i, word in enumerate(words):
            if word == '%f' or word[0] == '$':
                descs.append(word)
            else:
                new_desc = '$%s.%r' % (name, i)
                self.add_reduce(new_desc, word)
                descs.append(new_desc)

        if len(words) == 2:
            self.add_expand(unslashed_name,
                            descs[0],
                            descs[1],
                            f)
        else:
            self.add_expand('$%s.0t1' % name,
                            descs[0],
                            descs[1])
            for i in range(2, len(words)-1):
                self.add_expand('$%s.0t%r' % (name, i),
                                '$%s.0t%r' % (name, i-1),
                                descs[i])
            self.add_expand(unslashed_name,
                            '$%s.0t%r' % (name, len(words)-2),
                            descs[-1],
                            f)
         
        self.__sphinx_config.add_complex_rule(name, s, is_expression)

    def _update_min(self, f, current_min, current_argmin, current_argmin_temp, hyp):
        try:
            if f:
                new_argmin = f(current_argmin_temp)
                if type(new_argmin) is list:
                    return new_argmin, hyp
                else:
                    return [new_argmin], hyp
            else:
                return current_argmin_temp, hyp
        except:
            return current_argmin, current_min
        
    
    def _known(self, words, desc, C, arg_C, G, l, i):

        current_min = float('inf')
        current_argmin = arg_C[desc][l][i]

        if desc in self.__expands:
            for k in range(0, l):
                for (l_desc, r_desc), f in self.__expands[desc]:
                    hyp = C[l_desc][k][i] + C[r_desc][l-k][i+k]
                    if hyp < current_min:
                        current_argmin_temp = arg_C[l_desc][k][i] + arg_C[r_desc][l-k][i+k]
                        current_argmin, current_min = self._update_min(f,
                                                                       current_min,
                                                                       current_argmin,
                                                                       current_argmin_temp,
                                                                       hyp)

        nearest = {}
        for word in words[i:i+l]:
            new_nearest = self.proximity_dict.find_nearest(word)
            for k, v in new_nearest:
                if k not in nearest:
                    nearest[k] = v, word
                else:
                    if nearest[k][0] > v:
                        nearest[k] = v, word
            nearest[word] = 0, word

        if desc in self.__reduces:
            for word, formula in self.__reduces[desc]:
                hyp = self.proximity_dict.word_delete_cost(word) + G[i][l]
                if hyp < current_min:
                    current_min = hyp
                    if formula is None:
                        current_argmin = []
                    else:
                        current_argmin = [formula]
                if word in nearest:
                    hyp = nearest[word][0] + G[i][l] - self.proximity_dict.word_delete_cost(nearest[word][1])
                    if hyp < current_min:
                        current_min = hyp
                        if formula is None:
                            current_argmin = []
                        else:
                            current_argmin = [formula]

        arg_C[desc][l][i] = current_argmin
        
        return current_min
    
    def myers(self, s):

        words = s.split(' ')
        N = len(words)

        #Initialisation de G
        G = [[0] for _ in range(N+1)]
        for i in range(N):
            G[i].append(self.proximity_dict.word_delete_cost(words[i]))
            for j in range(i+1, N):
                G[i].append(G[i][-1] + self.proximity_dict.word_delete_cost(words[j]))

        #Initialisation de C
        C = { desc: [ [float('inf') for _1 in range(N+1-_2)] for _2 in range(N+1) ]
              for desc in self.__descriptors }
        arg_C = { desc: [ [ [] for _1 in range(N+1-_2) ] for _2 in range(N+1) ]
              for desc in self.__descriptors }

        for l in range(0, N+1):
            for i in range(0, N-l+1):
                heap = heapdict()
                for desc in self.__descriptors:
                    heap[desc] = C[desc][l][i] \
                                 = self._known(words, desc, C, arg_C, G, l, i)
                while heap:
                    desc, _ = heap.popitem()
                    if desc in self.__expands:
                        for key in heap:
                            if key not in self.__expands:
                                continue
                            for (desc1, desc2), f in self.__expands[key]:
                                if desc1 == desc or desc2 == desc:
                                    hyp1 = C[desc1][l][i] + C[desc2][0][0]
                                    hyp2 = C[desc2][l][i] + C[desc1][0][0]
                                    if hyp1 < C[key][l][i]:
                                        argmin_temp = arg_C[desc1][l][i] + arg_C[desc2][0][0]
                                        arg_C[key][l][i], C[key][l][i] = self._update_min(f,
                                                                                          C[key][l][i],
                                                                                          arg_C[key][l][i],
                                                                                          argmin_temp,
                                                                                          hyp1)
                                        heap[key] = C[key][l][i]
                                    if hyp2 < C[key][l][i]:
                                        argmin_temp = arg_C[desc2][l][i] + arg_C[desc1][0][0]
                                        arg_C[key][l][i], C[key][l][i] = self._update_min(f,
                                                                                          C[key][l][i],
                                                                                          arg_C[key][l][i],
                                                                                          argmin_temp,
                                                                                          hyp2)
                                        heap[key] = C[key][l][i]
                    if desc in self.__expression_descriptors and '%f' in heap:
                        if C[desc][l][i] < C['%f'][l][i]:
                            heap['%f'] = C['%f'][l][i] = C[desc][l][i]
                            arg_C['%f'][l][i] = arg_C[desc][l][i]
        
        return arg_C['%f'][N][0]
