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
        self.d = {"expression"}

    def add_simple_rule(self, name, l, is_expression=False):
        """Traite et stocke DES nouvelles règles simples (càd mots unique, n'utilisant pas déjà
        d'autres expressions ou variables existantes)
        Si is_expression==True, considérée aussi comme une description possible d'une <expression>
        """
        if is_expression:
            self.expressions = self.expressions | set(l)
            self.d = self.d | set(l)
        else:
            # On reste vigilant à l'absence possible d'initialisation
            if name in self.rules:
                self.rules[name] = self.rules[name] | set(l)
            else:
                self.rules[name] = set(l)
                self.d.add(name)

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
                self.d.add(wrd[1:])
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

    # Comparaison d'un mot utilisé dans la grammaire avec une ligne lue dans le fr_dict. Renvoie un booléen.
    def wrd_compared_to_line(word, line):
        # Il faut que le début de la ligne soit le mot, suivi d'un ESPACE ou d'une PARENTHESE
        return line.startswith(word) and (line[len(word) +1] == "(" or line[len(word) +1 ] == " ")

    #Retourne une chaine de caractère comprenant le mot, suivi de sa phonétique. Permet d'enlever les indices d'occurences multiples.
    def wrd_with_pronounciation(word,line):
        #!! On suppose word dans présent la ligne.
        #Le retour chariot est inclus. 
        line_nxt=line.strip(word)
        wrd_with_pro=word
        if line_nxt[0]=="(":
            line_nxt=line_nxt.partition(")")[2]
        wrd_with_pro+=line_nxt
        return wrd_with_pro


    def update_config_files(self):
        """Ecriture des fichiers .dict et .jsgf
        !!! Ecrase le contenue à chaque MAJ !!!
        """
        # Ecriture du fichier s2m.jsgf (grammaire)
        grammar = os.path.join("s2m", "core", "sphinx", "s2m.jsgf")
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
        wrds = list(self.d).sort()
        # Les mots commençant par "é" ou "è" sont bien triés en fin de liste, idem dans fr.dict.
        dictionnary_s2m = os.path.join("s2m", "core", "sphinx", "s2m.dict")
        dictionnary_fr = os.path.join("s2m", "core", "sphinx", "fr.dict")
        with open(dictionnary_s2m, "w") as dict_s2m:
            with open(dictionnary_fr, "r") as dict_fr:
                i, n = 0, wrds.length()
                while (i < n):
                line = dict_fr.readline()
                if wrd_compared_to_line(wrds[i], line):
                    dict_s2m.write(wrd_with_pronounciation(wrds[i],line))
                    i += 1
