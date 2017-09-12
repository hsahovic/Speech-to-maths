#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""[PSC Speech-to-Math]
                    sphinx_config.py
*************************************************************
*La classe SphinxConfig de ce ficher                        *
*reçoit la description d'une grammaire,                     *
*calcule la liste des mots qu'elle comporte,                *
*et traite le tout pour générer un dictionnaire *.dict      * 
*et une grammaire *.jsgf dans le dossier "sphinx"           *
*                                                           *
*Pour cette version, pas de gestion des accents en inpu     *
*(UnicodeEncodeError)                                       *
**********************************************************"""



import codecs

class SphinxConfig:

    def __init__(self,name,v_jsgf,v):
        """Les règles seront stockées à la volée dans une liste chainée de chaînes de caractères
        v_jsgf désigne la version du fichier de règles
        v désigne la version du projet
        expressions : cas particulier, stockées dans un set(), avec la synthaxe finale (< >, mots, etc)
        rules : stockées dans un dictionnaires de set(), sans la synthaxe finale (sans les < >), ajoutée en fin
        d = dictionnaire, ensemble de tous les mots français utilisés
        """
        self.v = str(v_jsgf)
        self.name ="speech-to-math-v"+str(v)
        self.expressions = set()
        self.rules = {}
        self.d = {"expression"}
        
        
    def add_simple_rule(self,name, list, is_expression=False):
        """Traite et stocke DES nouvelles règles simples (càd mots unique, n'utilisant pas déjà
        d'autres expressions ou variables existantes)
        Si is_expression==True, considérée aussi comme une description possible d'une <expression>
        """
        if is_expression==True:
            self.expression=self.expression|set(list)
            self.d=self.d|set(list)
        else :                          #On reste vigilant à l'absence possible d'initialisation
            if name in self.rules:
                self.rules[name]=self.rules[name]|set(list)
            else :
                self.rules[name]=set(list)
                self.d.add(name)
        
    def add_complex_rule(self,name, descriptor, is_expression=False):
        """Traite et stocke UNE nouvelle règle À LA FOIS (avec un name éventuellement déjà existant) se référant à
        d'autres expressions ou variables déjà ou possiblement existantes.
        Si is_expression==True, considérée aussi comme une description possible d'une <expression>
        """
        lst=descriptor.split(" ")       #Conversion en une liste de la description de la règle complexe.
        rule=[]                         #On va la stocker sous la nouvelle synthaxe dans une nouvelle liste....
        for str in lst:
            if(str=="%f"):
                rule.append("<expression>")
            elif(str[0]=="$"):
                rule.append("<"+str[1:]+">")
                self.d.add(str[1:])
            elif(str!="%f" and str[0]!="$"):
                rule.append(str)
                self.d.add(str)
        rule_str=" ".join(rule)         #....qui ensuite est repassée en str et stockée dans le set approprié
        if is_expression==True:
            self.expressions.add(rule_str)
        else :
            if name in self.rules:
                self.rules[name].add(rule_str)
            else :
                self.rules[name]=set(rule_str)
                self.d.add(name)
    
    def update_config_files(self):
        """Ecriture des fichiers .dict et .jsgf
        !!! Ecrase le contenue à chaque MAJ !!!
        """
        jsgf=open("s2m.jsgf","w")       #Ecriture du fichier s2m.jsgf (grammaire)
        jsgf.write("#JSGF V"+self.v+";")
        jsgf.write("\n\n"+"grammar "+self.name)
        expressions_str="public <expression> = "+(" | ".join(self.expressions))+";"
        jsgf.write("\n\n"+expressions_str)
        for name in self.rules.keys():
            rule_str="<"+name+"> = "+(" | ".join(self.rules[name]))+";"
            jsgf.write("\n\n"+rule_str)
        jsgf.close()
        dico=list(self.d).sort()                   #Tri de l'ensemble des mots français utilisés
        #dict=open("s2m.dict","w")       #Ecriture du fichuer s2m.dict (dico) RESTE À FAIRE
        #dict_fr=open("fr.dict","r")
        #....
        #dict.close()
        #dict_fr.close()



