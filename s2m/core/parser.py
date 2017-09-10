"""[PSC Speech-to-Math]           (Streichholzschaechtelchen)e
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

class Token:

    def __init__(self, tag, formula=None):

        if type(tag) != str:
            raise TypeError('Token tag must be a string, not %r.' % tag)
        elif formula and not type(formula) == list:
            raise TypeError('Token formula must be a list, not %r.' % formula)
        else:
            self.__tag, self.__formula = tag, formula

    def __getattr__(self, p):

        from formulae import Formula

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

        
class Parser:

    def __init__(self):

        self.__expands = []
        self.__reduces = []
        self.__aux = {}
        self.__names = []
        
    def add_expand(self, f):

        self.__expands.append(f)

    def add_reduce(self, f):

        self.__reduces.append(f)

    def add_easy_reduce(self, name, d, f):

        import parser_lambdas
        
        if name in self.__names:
            raise ValueError('Name %r is already the name of a rule.' % name)
        else:
            self.__names.append(name)

        self.add_reduce(parser_lambdas.reduce_1(name, d, f))

    def add_complex_rule(self, name, s, f):

        import parser_lambdas
        
        if name in self.__names:
            raise ValueError('Name %r is already the name of a rule.' % name)
        else:
            self.__names.append(name)
            
        words = s.split(' ')
        if len(words) < 2:
            raise ValueError('String describing a complex rule must be composed of at least two words, unlike %r.' % s)
        
        for i,word in enumerate(words):
            if word == '%f' or word[0] == '$':
                continue
            self.add_reduce(parser_lambdas.reduce_2(name, i, word))

        if len(words) == 2:
            
            if words[0] == '%f':
                if words[1] == '%f':
                    self.add_expand(parser_lambdas._2_ff(name, f))
                elif words[1][0] == '$':
                    self.add_expand(parser_lambdas._2_ft(name, words[1][1:], f))
                else:
                    self.add_expand(parser_lambdas._2_fw(name, f))
            elif words[0][0] == '$':
                if words[1] == '%f':
                    self.add_expand(parser_lambdas._2_tf(name, words[0][1:], f))
                elif words[1][0] == '$':
                    self.add_expand(parser_lambdas._2_tt(name, words[0][1:], words[1][1:], f))
                else:
                    self.add_expand(parser_lambdas._2_tw(name, words[0][1:], f))
            else:
                if words[1] == '%f':
                    self.add_expand(parser_lambdas._2_wf(name, f))
                elif words[1][0] == '$':
                    self.add_expand(parser_lambdas._2_wt(name, words[1][1:], f))
                else:
                    self.add_expand(parser_lambdas._2_ww(name, f))

        else:
            
            if words[0] == '%f':
                if words[1] == '%f':
                    self.add_expand(parser_lambdas._1_ff(name))
                elif words[1][0] == '$':
                    self.add_expand(parser_lambdas._1_ft(name, words[1][1:]))
                else:
                    self.add_expand(parser_lambdas._1_fw(name))
            elif words[0][0] == '$':
                if words[1] == '%f':
                    self.add_expand(parser_lambdas._1_tf(name, words[0][1:]))
                elif words[1][0] == '$':
                    self.add_expand(parser_lambdas._1_tt(name, words[0][1:], words[1][1:]))
                else:
                    self.add_expand(parser_lambdas._1_tw(name, words[0][1:]))
            else:
                if words[1] == '%f':
                    self.add_expand(parser_lambdas._1_wf(name))
                elif words[1][0] == '$':
                    self.add_expand(parser_lambdas._1_wt(name, words[1][1:]))
                else:
                    self.add_expand(parser_lambdas._1_ww(name))
                
            for i in range(2,len(words)-1):
                if words[i] == '%f':
                    self.add_expand(parser_lambdas.i_f(name, i))
                elif words[i][0] == '$':
                    self.add_expand(parser_lambdas.i_t(name, i, words[i][1:]))
                else:
                    self.add_expand(parser_lambdas.i_w(name, i))

            if words[len(words)-1] == '%f':
                self.add_expand(parser_lambdas.l_f(name, len(words)-1, f))
            elif words[len(words)-1][0] == '$':
                self.add_expand(parser_lambdas.l_t(name, len(words)-1, words[-1][1:], f))
            else:
                self.add_expand(parser_lambdas.l_w(name, len(words)-1, f))
        
    def cky(self, s):

        words = s.split(' ')
        lines = []
        line = []
        
        for word in words:
            cell = []
            for f in self.__reduces:
                word_parsed = f(word)
                if word_parsed:
                    cell.append(word_parsed)
            if cell:
                line.append(cell)
            else:
                raise ValueError('Syntax error: Word %r is not defined.' % word) 
        lines.append(line)

        for i in range(2, len(words)+1):
            line = []
            for j in range(0, len(words)+1-i):
                cell = []
                for k in range(1, i):
                    for lhs in lines[k-1][j]:
                        for rhs in lines[i-k-1][j+k]:
                            for f in self.__expands:
                                words_parsed = f(lhs, rhs)
                                if words_parsed:
                                    cell.append(words_parsed)
                line.append(cell)
            lines.append(line)
           
        return [tok.formula[0] for tok in lines[-1][0] if len(tok.formula) == 1]
