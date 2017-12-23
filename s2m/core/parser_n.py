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

from functools import reduce

class Token:

    def __init__(self, tag, formula=None):

        if type(tag) != str:
            raise TypeError('Token tag must be a string, not %r.' % tag)
        elif formula and not type(formula) == list:
            raise TypeError('Token formula must be a list, not %r.' % formula)
        else:
            self.__tag, self.__formula = tag, formula

    def __getattr__(self, p):

        from s2m.core.formulae import Formula

        if p == 'tag':
            return self.__tag
        elif p == 'formula':
            return self.__formula
        elif p == 'is_full_formula':
            return self.__formula \
                   and len(self.__formula) == 1 \
                   and issubclass(self.__formula[0].__class__, Formula)
        else:
            raise AttributeError

    def __eq__(self, other):
        
        if other and isinstance(other, Token):
            return other.tag == self.__tag and other.formula == self.__formula
        return False
    
    def __hash__(self):

        if self.__formula:
            return reduce(lambda a, b: a ^ hash(b), self.__formula, hash(self.__tag))
        else:
            return hash(self.__tag)


class Parser:

    def __init__(self):

        self.__expands = {}
        self.__reduces = {}
        self.__aux = {}
        self.__names = []
        self.__sphinx_config = SphinxConfig(S2M_GRAMMAR_NAME,
                                            S2M_GRAMMAR_VERSION,
                                            S2M_VERSION)

    def __getattr__(self, p):

        if p == 'sphinx_config':
            return self.__sphinx_config
        else:
            raise AttributeError
        
    def add_expand(self, name, word1, word2, f=None):

        exp = (name, f)
        words12 = (word1, word2)
        if words12 in self.__expands:
            self.__expands[words12].append(exp)
        else:
            self.__expands[words12] = [exp]

    def add_reduce(self, name, word, formula=None):

        tok = Token(name, [formula] if formula else [])
        if word in self.__reduces:
            self.__reduces[word].append(tok)
        else:
            self.__reduces[word] = [tok]

    def add_easy_reduce(self, name, d, f, is_expression=False):

        import s2m.core.parser_lambdas as parser_lambdas
        
        if name in self.__names:
            raise ValueError('Name %r is already the name of a rule.' % name)
        else:
            self.__names.append(name)

        k = 0

        for key, val in d.items():
            words = key.split(' ')
            if len(words) == 0:
                raise ValueError('String to be recognized by the parser must be non-empty.')
            elif len(words) == 1:
                self.add_reduce(name, key, f(val))
            elif len(words) == 2:
                self.add_reduce('%s/%r.0' % (name, k), words[0])
                self.add_reduce('%s/%r.1' % (name, k), words[1])
                self.add_expand(name,
                                '$%s/%r.0' % (name, k),
                                '$%s/%r.1' % (name, k),
                                lambda _: f(val))
                k += 1
            else:
                for i, word in enumerate(words):
                    self.add_reduce('%s/%r.%r' % (name, k, i), words[i])
                self.add_expand('%s/%r.0t1' % (name, k),
                                '$%s/%r.0' % (name, k),
                                '$%s/%r.1' % (name, k))
                for i in range(2, len(words)-1):
                    self.add_expand('%s/%r.0t%r' % (name, k, i),
                                    '$%s/%r.0t%r' % (name, k, i-1),
                                    '$%s/%r.%r' % (name, k, i))
                self.add_expand(name,
                                '$%s/%r.0t%r' % (name, k, len(words)-2),
                                '$%s/%r.%r' % (name, k, len(words)-1),
                                lambda _: f(val))
                k += 1

        self.__sphinx_config.add_simple_rule(name, d.keys(), is_expression)

    def add_complex_rule(self, name, s, f, is_expression=True):

        if name in self.__names:
            raise ValueError('Name %r is already the name of a rule.' % name)
        else:
            self.__names.append(name)
            
        words = s.split(' ')
        if len(words) < 2:
            raise ValueError('String describing a complex rule must be composed of at least two words, unlike %r.' % s)        

        for i, word in enumerate(words):
            if word == '%f' or word[0] == '$':
                continue
            self.add_reduce('%s.%r' % (name, i), word)

        if len(words) == 2:
            self.add_expand(name,
                            '$%s.0' % name,
                            '$%s.1' % name)
        else:
            self.add_expand('%s.0t1' % name,
                            '$%s.0' % name,
                            '$%s.1' % name)
            for i in range(2, len(words)-1):
                self.add_expand('%s.0t%r' % (name, i),
                                '$%s.0t%r' % (name, i-1),
                                '$%s.%r' % (name, i))
            self.add_expand(name,
                            '$%s.0t%r' % (name, len(words)-2),
                            '$%s.%r' % (name, len(words)-1),
                            f)
       
        self.__sphinx_config.add_complex_rule(name, s, is_expression)

    def myers(self, s):
        pass
        
    def cky(self, s):

        THRESHOLD = 0.75
        MAXCOUNT = 8

        words = s.split(' ')
        lines = []
        line = []

        for word in words:
            cell = set()
            for f in self.__reduces:
                word_parsed = f(word)
                if word_parsed:
                    cell.add(word_parsed)
            if cell:
                line.append(cell)
            else:
                raise ValueError('Syntax error: Word %r is not defined.' % word) 
        lines.append(line)

        for i in range(2, len(words)+1):
            line = []
            for j in range(0, len(words)+1-i):
                cell_buf = []
                cell = set()
                max_evaluation = 0
                for k in range(1, i):
                    for lhs in lines[k-1][j]:
                        for rhs in lines[i-k-1][j+k]:
                            for f in self.__expands:
                                words_parsed = f(lhs, rhs)
                                if words_parsed:
                                    if words_parsed.is_full_formula:
                                        evaluation = words_parsed.formula[0].evaluation()
                                        cell_buf.append((words_parsed, evaluation))
                                        if evaluation > max_evaluation:
                                            max_evaluation = evaluation
                                    else:
                                        cell.add(words_parsed)
                cell_buf.sort(key=lambda x:x[1], reverse=True)
                for k, v in cell_buf[:MAXCOUNT]:
                    if v > THRESHOLD * max_evaluation:
                        cell.add(k)
                line.append(cell)
            lines.append(line)
            
        return sorted([tok.formula[0] for tok in lines[-1][0] if tok.is_full_formula],
                       key=lambda x:x.evaluation(), reverse=True)
