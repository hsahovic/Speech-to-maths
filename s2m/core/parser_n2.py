from s2m.core.sphinx_config import SphinxConfig
from s2m.core.version import *
from s2m.core.utils import _unslash
from s2m.core.bwoq import BoundedWriteOnlyQueue
from s2m.core.formulae import Formula
from s2m.core.prefix_dict import PrefixDict

from functools import reduce
from re import match
#Priority queue implementation by Daniel Stutzbach
from heapdict import heapdict

from time import time

class Parser:

    def __init__(self, proximity_dict, PlaceHolder=None):

        self.__expands = {}
        self.__reduces = {}
        self.__rule_names = []
        self.__descriptors = {'%f'}
        self.__expression_descriptors = set()
        self.__sphinx_config = SphinxConfig(S2M_GRAMMAR_NAME,
                                            S2M_GRAMMAR_VERSION,
                                            S2M_VERSION)
        self.__proximity_dict = proximity_dict
        self.__help_dict = PrefixDict(reverse=False)
        self.__PlaceHolder = PlaceHolder

    def __getattr__(self, p):

        if p == 'sphinx_config':
            return self.__sphinx_config
        elif p == 'proximity_dict':
            return self.__proximity_dict
        elif p == 'help_dict':
            return self.__help_dict
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
            
    def add_easy_reduce(self, name, d, f, is_expression=False, no_pregen=False):

        self._validate_name(name, is_expression)

        unslashed_name = _unslash('$' + name)
        
        k = 0

        for key, val in d.items():
            words = key.split(' ')
            if len(words) == 0:
                raise ValueError('String to be recognized by the parser must be non-empty.')
            elif len(words) == 1:
                if no_pregen:
                    self.add_reduce(unslashed_name, key, (f, val))
                else:
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

    def _compare(self, x, y, sess, document, context_formula=None, placeholder_id=1):

        if x[1] > y[1]:
            return True
        elif x[1] < y[1]:
            return False
        elif len(x[0]) == 1 and len(y[0]) == 1 \
             and isinstance(x[0][0], Formula) and isinstance(y[0][0], Formula) \
        and x[0][0].evaluation(sess, document, context_formula, placeholder_id) < y[0][0].evaluation(sess, document, context_formula, placeholder_id):
            return True
        else:
            return False

    def _assemble(self, f, formulae):

        if f:
            new_formula = f(formulae)
            if type(new_formula) is list:
                return new_formula
            else:
                return [new_formula]
        else:
            return formulae

    def _combine(self, l_queue, r_queue, dest, f):

        min_score_hyp = l_queue.min_value() + r_queue.min_value()
        if dest.will_be_rejected(min_score_hyp):
            return

        for l_formula, l_score in l_queue:
            for r_formula, r_score in r_queue:
                score_hyp = l_score + r_score
                if dest.will_be_rejected(score_hyp):
                    continue
                formulae = l_formula + r_formula
                try:
                    new_formula = self._assemble(f, formulae)
                except:
                    pass
                else:
                    dest[new_formula] = score_hyp

    def _nearest(self, words, l, i):
        
        nearest = {}
        for word in words[i:i+l]:
            new_nearest = self.proximity_dict.find_nearest(word)
            delete_cost = self.proximity_dict.word_delete_cost(word)
            for k, v in new_nearest:
                if k not in nearest:
                    nearest[k] = v - delete_cost
                else:
                    if nearest[k] > v - delete_cost:
                        nearest[k] = v - delete_cost
            nearest[word] = - delete_cost
        return nearest
    
    def _known(self, desc, C, G, nearest, l, i):

        if desc in self.__expands:
            for k in range(0, l):
                for (l_desc, r_desc), f in self.__expands[desc]:
                    self._combine(C[l_desc][k][i],
                                  C[r_desc][l-k][i+k],
                                  C[desc][l][i],
                                  f)

        if desc in self.__reduces:
            for word, formula in self.__reduces[desc]:
                hyp_score = self.proximity_dict.word_delete_cost(word) + G[i][l]
                if word in nearest[l][i]:
                    hyp_score2 = nearest[l][i][word] + G[i][l]
                    if hyp_score2 < hyp_score:
                        hyp_score = hyp_score2
                if formula is None:
                    C[desc][l][i][ [] ] = hyp_score
                elif type(formula) is tuple:
                    func, val = formula
                    C[desc][l][i][ [func(val)] ] = hyp_score
                else:
                    C[desc][l][i][ [formula] ] = hyp_score

        C[desc][l][i].prune()
        return C[desc][l][i].min_value()


    def myers(self, s, sess, document, context_formula=None, placeholder_id=0, threshold_factor=2, verbose=False):

        if verbose:
            _time = time()

        #Ajout d'un curseur en fin de chaîne
        placeholder = self.__PlaceHolder()
        placeholder_name = placeholder.transcription()
        s += ' ' + placeholder_name
        
        words = s.split(' ')
        N = len(words)

        #Initialisation de G
        G = [[0] for _ in range(N+1)]
        for i in range(N):
            G[i].append(self.proximity_dict.word_delete_cost(words[i]))
            for j in range(i+1, N):
                G[i].append(G[i][-1] + self.proximity_dict.word_delete_cost(words[j]))

        #Initialisation de C
        C = { desc: [ [BoundedWriteOnlyQueue(comparator=self._compare,
                                             args=(sess, document, context_formula, placeholder_id))
                       for _1 in range(N+1-_2)] for _2 in range(N+1) ]
              for desc in self.__descriptors }

        #Initialisation de nearest
        nearest = [ [self._nearest(words, l, i) for i in range(N+1-l)]
                    for l in range(N+1) ]

        if verbose:
            print("Initializations took: %rs" % (time() - _time))
            _time = time()
            _time2 = 0
            _time3 = 0

        for l in range(0, N+1):
            for i in range(0, N-l+1):
                current_min = float('inf')
                if verbose:
                    _time2 -= time()
                heap = heapdict()
                for desc in self.__descriptors:
                    C[desc][l][i].set_threshold(threshold_factor * current_min)
                    score = self._known(desc, C, G, nearest, l, i)
                    if desc in self.__expands:
                        heap[desc] = score
                    if score < current_min:
                        current_min = score
                if verbose:
                    _time2 += time()
                    _time3 -= time()
                for desc in self.__expression_descriptors:
                    for formula, score in C[desc][l][i]:
                        C['%f'][l][i][formula] = score
                    C['%f'][l][i].prune()
                while heap:
                    desc, _ = heap.popitem()
                    for key in heap:
                        for (desc1, desc2), f in self.__expands[key]:
                            if desc1 == desc or desc2 == desc:
                                self._combine(C[desc1][l][i],
                                              C[desc2][0][0],
                                              C[key][l][i],
                                              f)
                                self._combine(C[desc2][l][i],
                                              C[desc1][0][0],
                                              C[key][l][i],
                                              f)
                                C[key][l][i].prune()
                                heap[key] = C[key][l][i].min_value()
                    if desc in self.__expression_descriptors:
                        for formula, score in C[desc][l][i]:
                            C['%f'][l][i][formula] = score
                        C['%f'][l][i].prune()
                if verbose:
                    _time3 += time()

        if verbose:
            print("Main procedure took: %rs" % (time() - _time))
            print("... of which _known took: %rs" % _time2)
            print("... and everything else: %rs" % _time3)
            _time = time()

        if C['%f'][N-1][0].min_value() > 0. \
           and C['%f'][N][0].min_value() == 0.:
            return_list = C['%f'][N][0].sorted_list()
        else:
            return_list = C['%f'][N-1][0].sorted_list()

        if verbose:
            print("Output took: %rs" % (time() - _time))

        return return_list
