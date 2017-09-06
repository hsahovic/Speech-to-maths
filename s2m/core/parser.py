class Token:

    def __init__(self, tag, formula=None):

        if type(tag) != str:
            raise TypeError('Token tag must be a string, not %r.' % name)
        elif formula and not type(formula) == list:
            raise TypeError('Token formula must be a list, not %r.' % formula)
        else:
            self.__tag, self.__formula = tag, formula

    def __getattr__(self, p):

        if p == 'tag':
            return self.__tag
        elif p == 'formula':
            return self.__formula
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

    def add_aux(self, name, f):

        if name in self.__names:
            raise ValueError(('Name %r is already the name of a complex rule, cannot be the' \
                              + ' name of an auxiliary function.') % name)
        elif name in self.__aux.keys():
            raise ValueError('Name %r is already the name of an auxiliary function.')
        else:
            self.__aux[name] = f
        
    def add_complex_rule(self, name, s, f):

        if name in self.__names:
            raise ValueError('Name %r is already the name of a complex rule.' % name)
        else:
            self.__names.append(name)
            
        words = s.split(' ')
        if len(words) < 2:
            raise ValueError('String describing a complex rule must be composed of at least two words, unlike %r.' % s)
        
        add_reduce_model = 'self.add_reduce(lambda x: Token(\'%s.%r\') if x==\'%s\' else None)'
        for i,word in enumerate(words):
            if word == '%f' or word[0] == '$':
                continue
            my_add_reduce = add_reduce_model % (name, i, word)
            exec(my_add_reduce)

        if len(words) > 2:
            add_expand_model_0 = 'self.add_expand(lambda x,y,z: Token(\'%s.0t1\', %s + %s) if %s and %s else None)'
            if words[0] == '%f':
                aem_0a = 'x.formula'
                aem_0c = 'x.formula is not None'
            elif words[0][0] == '$':
                aem_0a = 'x.formula'
                aem_0c = 'x.tag == \'%s\'' % words[0][1:]
            else:
                aem_0a = '[]'
                aem_0c = 'x.tag == \'%s.0\'' % name
            if words[1] == '%f':
                aem_0b = 'y.formula'
                aem_0d = 'y.formula is not None'
            elif words[1][0] == '$':
                aem_0b = 'y.formula'
                aem_0d = 'y.tag == \'%s\'' % words[1][1:]
            else:
                aem_0b = '[]'
                aem_0d = 'y.tag == \'%s.1\'' % name
            exec(add_expand_model_0 % (name, aem_0a, aem_0b, aem_0c, aem_0d))

                
        add_expand_model_1 = 'self.add_expand(lambda x,y,z: Token(\'%s.0t%r\', x.formula + y.formula)' \
                             + ' if x.tag == \'%s.0t%r\' and y.formula is not None else None)'
        add_expand_model_2 = 'self.add_expand(lambda x,y,z: Token(\'%s.0t%r\', x.formula)' \
                             + ' if x.tag == \'%s.0t%r\' and y.tag == \'%s.%r\' else None)'
        add_expand_model_3 = 'self.add_expand(lambda x,y,z: Token(\'%s.0t%r\', x.formula)' \
                             + ' if x.tag == \'%s.0t%r\' and y.tag == \'%s\' else None)'

        for i in range(2,len(words)-1):
            if words[i] == '%f':
                my_add_expand = add_expand_model_1 % (name, i, name, i-1)
            elif words[i][0] == '$':
                my_add_expand = add_expand_model_3 % (name, i, name, i-1, words[i][1:])
            else:
                my_add_expand = add_expand_model_2 % (name, i, name, i-1, name, i)
            exec(my_add_expand)

        self.add_aux(name + '.aux', f)
        add_expand_model_4 = 'self.add_expand(lambda x,y,z: Token(\'%s\', [z[\'%s.aux\'](x.formula%s)])' \
                             + ' if x.tag == \'%s.0t%r\' and %s else None)'
        if words[len(words)-1] == '%f':
            aem_4a = ' + y.formula'
            aem_4b = 'y.formula is not None'
        elif words[len(words)-1][0] == '$':
            aem_4a = ' + y.formula'
            aem_4b = 'y.tag == \'%s\'' % words[len(words)-1][1:]
        else:
            aem_4a = ''
            aem_4b = 'y.tag == \'%s.%r\'' % (name, len(words)-1)
        exec(add_expand_model_4 % (name, name, aem_4a, name, len(words)-2, aem_4b))
        
    def cky(self, s):

        words = s.split(' ')
        lines = []
        line = []
        
        for word in words:
            cell = []
            for f in self.__reduces:
                word_parsed = f(word)
                if word_parsed is not None:
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
                                words_parsed = f(lhs, rhs, self.__aux)
                                if words_parsed is not None:
                                    cell.append(words_parsed)
                line.append(cell)
            lines.append(line)

        return [tok.formula[0] for tok in lines[-1][0] if len(tok.formula) == 1]
        
    def learn(self, F):

        import formulae

        if not issubclass(F, formulae.Formula):
            raise TypeError

        new_expands, new_reduces, new_aux, new_complex_rules = F.parsing_rules()

        for e in new_expands:
            self.add_expand(e)
        for r in new_reduces:
            self.add_reduce(r)
        for a in new_aux:
            self.add_aux(*a)
        for cr in new_complex_rules:
            self.add_complex_rule(*cr)
