"""[PSC Speech-to-Math]                              (loisft)
                    sphinx_config.py
*************************************************************
*La classe SphinxConfig de ce ficher reçoit la description  * 
*d'une grammaire, calcule la liste des mots qu'elle comporte*
*et traite le tout pour générer un dictionnaire *.dict et   *
*une grammaire *.jsgf dans le dossier "sphinx"              *
**********************************************************"""

import codecs
import os
import re
class SphinxConfig:

    def __init__(self, name, v_jsgf, v):
        """Les règles seront stockées à la volée dans une liste chainée de chaînes de caractères
        v_jsgf désigne la version du fichier de règles
        v désigne la version du projet
        expressions : cas particulier, stockées dans un set(), avec la synthaxe finale (< >, mots, etc)
        rules : stockées dans un dictionnaires de set(), sans la synthaxe finale (sans les < >), ajoutée en fin
        d = dictionnaire, ensemble de tous les mots français utilisés
        """
        self.v = str(v_jsgf)
        self.name = "speech-to-math-v" + str(v)
        self.expressions = set()
        self.rules = {}
        self.d = set()

    def add_simple_rule(self, name, l, is_expression=False):
        """Traite et stocke DES nouvelles règles simples (càd mots unique, n'utilisant pas déjà
        d'autres expressions ou variables existantes)
        Si is_expression==True, considérée aussi comme une description possible d'une <expression>
        """
        if is_expression:
            self.expressions |= set(l)
            self.d |= set(l)
        else:
            # On reste vigilant à l'absence possible d'initialisation
            if name in self.rules:
                self.rules[name] |= set(l)
            else:
                self.rules[name] = set(l)
            self.d |= set(l)

    def add_complex_rule(self, name, descriptor, is_expression=False):
        """Traite et stocke UNE nouvelle règle À LA FOIS (avec un name éventuellement déjà existant)
        se référant à d'autres expressions ou variables déjà ou possiblement existantes.
        Si is_expression==True, considérée aussi comme une description possible d'une <expression>
        """
        lst = descriptor.split(" ")
        # Conversion en une liste de la description de la règle complexe.
        # On va la stocker sous la nouvelle synthaxe dans une nouvelle liste....
        rule = []
        for wrd in lst:
            if wrd == "%f":
                rule.append("<expression>")
            elif wrd[0] == "$":
                rule.append("<%s>" % wrd[1:])
            else:
                rule.append(wrd)
                self.d.add(wrd)
        # ....qui ensuite est repassée en str et stockée dans le set approprié
        rule_str = " ".join(rule)
        if is_expression:
            self.expressions.add(rule_str)
        else:
            if name in self.rules:
                self.rules[name].add(rule_str)
            else:
                self.rules[name] = set([rule_str])
                self.d.add(name)

    def import_file(self, filename):
        """Importe le contenu d'un autre fichier .jsgf
           en vérifiant l'absence d'incompatibilités
           entre les deux descriptions"""
        
        comment_regex = re.compile(r'^\s*#.*;\s*$', re.UNICODE)
        header_regex = re.compile(r'^\s*grammar\s+[\w-]+\s*;\s*$', re.UNICODE)
        class_regex = re.compile(r'^\s*(?:public\s+)?<(\w+)>\s*=\s*(\S(?:.*\S)?)\s*;\s*$', re.UNICODE)
        whitespace_regex = re.compile(r'^\s*$', re.UNICODE)
        disjunction_regex = re.compile(r'\s*\|\s*', re.UNICODE)
        vocabulary_regex = re.compile(r'(?:[^\w<>]|\s*^)(\w+)(?=[^\w<>]|\s*$)', re.UNICODE)

        with open(filename, 'r') as jsgf:
            read_header = False
            while True:
                line = jsgf.readline()
                if not line:
                    break
                if comment_regex.match(line) \
                   or whitespace_regex.match(line):
                    continue
                elif header_regex.match(line):
                    read_header = True
                elif class_regex.match(line):
                    if not read_header:
                        raise RuntimeError('File %s shows no header before content.' % filename)
                    m = class_regex.match(line)
                    name, desc = m.group(1), m.group(2)
                    disj = disjunction_regex.split(desc)
                    if name == 'expression':
                        self.expressions |= set(disj)
                    elif name in self.rules:
                        self.rules[name] |= set(disj)
                    else:
                        self.rules[name] = set(disj)
                    v = vocabulary_regex.findall(desc)
                    self.d |= set(v)
                else:
                    raise RuntimeError('Line %r in file %s does not match the jsgf format.'
                                       % (line[:20], filename))

    # Retourne une chaine de caractère comprenant le mot, suivi de sa phonétique. Permet d'enlever les indices d'occurences multiples.
    def wrd_with_pronunciation(self, word, line):
        #!! On suppose word présent dans la ligne.
        # Le retour chariot est inclus.
        line_nxt = line.strip(word)
        wrd_with_pro = word
        if line_nxt[0] == "(":
            line_nxt = line_nxt.partition(")")[2]
        wrd_with_pro += line_nxt
        return wrd_with_pro

    def update_config_files(self, grammar=None, dictionary_s2m=None):
        """Ecriture des fichiers .dict et .jsgf
        !!! Ecrase le contenue à chaque MAJ !!!
        """
        # Ecriture du fichier s2m.jsgf (grammaire)
        grammar = grammar or os.path.join("s2m", "core", "sphinx", "s2m.jsgf")
        with open(grammar, "w") as jsgf:
            jsgf.write("#JSGF V%s;" % self.v)
            jsgf.write("\n\ngrammar %s;" % self.name)
            if self.expressions:  # Comportement à préciser dans le cas où expressions est vide
                expressions_str = "public <expression> = %s;" % " | ".join(
                    self.expressions)
                jsgf.write("\n\n" + expressions_str)
            for name in self.rules.keys():
                rule_str = "<%s> = %s;" % (name, " | ".join(self.rules[name]))
                jsgf.write("\n\n" + rule_str)

        # Ensemble des mots français utilisés, triés.
        # Les mots commençant par "é" ou "è" sont bien triés en fin de liste, idem dans fr.dict.
        wrds = sorted(list(self.d))
        # Les mots commençant par "é" ou "è" sont bien triés en fin de liste, idem dans fr.dict.
        # On supose que les mots sont tous présents dans fr.dict.
        dictionary_s2m = dictionary_s2m or os.path.join("s2m", "core", "sphinx", "s2m.dict")
        dictionary_fr = os.path.join("s2m", "core", "sphinx", "fr.dict")
        first_word_regex = re.compile(r'^[\w-]+', re.UNICODE)
        with open(dictionary_s2m, "w") as dict_s2m:
            with open(dictionary_fr, "r") as dict_fr:
                i, n, f = 0, len(wrds), False
                while i < n:
                    line = dict_fr.readline()
                    word = first_word_regex.match(line)
                    if word:
                        word = word.group()
                    else:
                        continue
                    if word == wrds[i]:
                        dict_s2m.write(line)
                        f = True
                    elif word > wrds[i]:
                        if f:
                            if i == len(wrds)-1:
                                break
                            i += 1
                            if word == wrds[i]:
                                dict_s2m.write(line)
                            else:
                                f = False
                        else:
                            raise RuntimeError('Word %r cannot be found in dictionary.' % wrds[i])
