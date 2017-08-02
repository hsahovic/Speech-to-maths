"""[PSC Speech-to-Math]                (Streichholzschaechtelchen)
                       number_parser.py
  ***************************************************************
  *Convertit les "nombres en lettres" en "nombres en chiffres". *
  *Supporte les nombres decimaux positifs inferieurs à 10e66-1. *
  *Syntaxe d'appel : parse_number('quarante deux')              *
  *Sortie : un flottant ou None                                 *
  *Les mots 'vingt', 'cent', 'million', etc. ne s'accordent pas.*
  *La partie decimale peut etre dictee en blocs de taille qcque.*
  *Aucun trait d'union ni accent n'est utilise.                 *
  ***********************************************************"""

##UTILS

words_to_parse = []
len_words_to_parse = 0
i = 0

n2to9 = {'deux':2, 'trois':3, 'quatre':4, 'cinq':5,
         'six':6, 'sept':7, 'huit':8, 'neuf':9}
n7to9 = {'sept':7, 'huit':8, 'neuf':9}
n20to50 = {'vingt':2, 'trente':3, 'quarante':4,
           'cinquante':5, 'septante':7, 'octante':8,
           'nonante':9}
n12to16 = {'douze':12, 'treize':13, 'quatorze':14,
           'quinze': 15, 'seize': 16}
e3s = {'million':6, 'milliard':9, 'billion':12, 'billard':15,
       'trillion':18, 'trilliard':21, 'quatrillon':24, 'quadrillard':27,
       'quintillion':30, 'quintillard':33, 'sextillion':36, 'sextillard':39,
       'septillion':42, 'septilliard':45, 'octillon':48, 'octilliard':51,
       'nonillion':54, 'nonilliard':57, 'decillion':60, 'decilliard':63}

def eof(o=0):
    """Indique si le caractere a la position i+o se trouve au-dela de la
       fin de chaine ou correspond a la position de la virgule"""
    return i+o >= len_words_to_parse or words_to_parse[i+o] == 'virgule'

def log(x):
    """Calcule la partie entiere du log decimal d'un entier > 0"""
    if x < 10:
        return 1
    else:
        return 1 + log(x // 10)

##CORE

def parse_number(words):
    """Fonction mère -- renvoie le nombre correspondant à la chaine
       Effectue une passe unique sur le texte a analyser"""
    global words_to_parse, i, len_words_to_parse
    words_to_parse = words.split(' ')
    len_words_to_parse = len(words_to_parse)
    i = 0
    d = 0
    b, v = parse_integer()
    if b \
       and (i == len_words_to_parse or words_to_parse[i] == 'virgule'):
        if i < len_words_to_parse:
            i += 1
        if eof() and words_to_parse[i-1] == 'virgule':
            return None
        while i < len_words_to_parse:
            c, w = parse_integer()
            if c:
                d -= log(w)
                v += w * (10 ** d)
            else:
                return None
        return v
    else:
        return None

def parse_integer():
    """Fonction auxiliaire -- renvoie le prochain entier lisible sur
       la chaine"""
    global words_to_parse, i
    j = i
    k = 1764
    a = 0
    while(True):
        b, v = ls999()
        if b:
            if not eof():
                if words_to_parse[i] == 'mille':
                    i += 1
                    if not eof():
                        c, w  = ls999()
                        return c, a + v * 1000 + w
                    else:
                        return True, a + v * 1000
                elif words_to_parse[i] in e3s.keys() \
                     and e3s[words_to_parse[i]] < k:
                    k = e3s[words_to_parse[i]]
                    i += 1
                    if eof():
                        return True, a + v * (10 ** k)
                    else:
                        a += v * (10 ** k)
                else:
                    return True, v
            else:
                return True, a + v
        elif not eof() and words_to_parse[i] == 'mille':
            i += 1
            if not eof():
                c, w = ls999()
                return c, a + 1000 + w
            else:
                return True, a + 1000
        else:
            return False, 0

def ls999():
    """Construction des nombres <= a 999"""
    global words_to_parse, i, n2to9
    if words_to_parse[i] == 'cent':
        i += 1
        if not eof():
            b, v = ls99()
            return b, 100 + v
        else:
            return True, 100
    elif not eof(1) \
         and words_to_parse[i] in n2to9.keys() \
         and words_to_parse[i+1] == 'cent':
        w = n2to9[words_to_parse[i]]
        i += 2
        if not eof() \
           and not words_to_parse[i] == 'mille' \
           and not words_to_parse[i] in e3s.keys():
            b, v = ls99()
            return b, w * 100 + v
        else:
            return True, w * 100
    else:
        return ls99()

def p6080(p80):
    """Construction des nombres >= a 60 et <= a 99"""
    global n2to9, n7to9, n12to16, i
    if eof():
        return True, 60
    i += 1
    if not eof() \
       and not p80 \
       and words_to_parse[i-1] == 'et':
        i += 1
        if words_to_parse[i-1] == 'un':
            return True, 61
        elif words_to_parse[i-1] == 'onze':
            return True, 71
        else:
            return False, 0
    elif not eof() \
         and words_to_parse[i-1] == 'dix' \
         and words_to_parse[i] in n7to9.keys():
            i += 1
            return True, 70 + n7to9[words_to_parse[i-1]]
    elif words_to_parse[i-1] == 'dix':
        return True, 70
    elif words_to_parse[i-1] in n2to9.keys():
        return True, 60 + n2to9[words_to_parse[i-1]]
    elif words_to_parse[i-1] in n12to16.keys():
        return True, 60 + n12to16[words_to_parse[i-1]]
    elif p80 and words_to_parse[i-1] == 'un':
        return True, 61
    elif p80 and words_to_parse[i-1] == 'onze':
        return True, 71
    else:
        i -= 1
        return True, 60
        
def ls99():
    """Construction des nombres <= a 99"""
    global words_to_parse, i, n2to9, n12to16, n20to50
    if words_to_parse[i] in n20to50.keys():
        if not eof(1) \
           and words_to_parse[i+1] in n2to9.keys():
            v = n20to50[words_to_parse[i]] * 10 + n2to9[words_to_parse[i+1]]
            i += 2
            return True, v
        elif not eof(2) \
             and words_to_parse[i+1] == 'et' \
             and words_to_parse[i+2] == 'un':
            i += 3
            return True, n20to50[words_to_parse[i-3]] * 10 + 1
        else:
            i += 1
            return True, n20to50[words_to_parse[i-1]] * 10
    elif words_to_parse[i] == 'soixante':
        i += 1
        return p6080(False)
    elif not eof(1) \
         and words_to_parse[i] == 'quatre' \
         and words_to_parse[i+1] == 'vingt':
        i += 2
        b, v = p6080(True)
        return b, v + 20
    else:
        return ls19()

def ls19():
    """Construction des nombres <= a 19"""
    global words_to_parse, i, n2to9, n12to16
    i += 1
    if words_to_parse[i-1] == 'zero':
        return True, 0
    elif words_to_parse[i-1] == 'un':
        return True, 1
    elif words_to_parse[i-1] == 'onze':
        return True, 11
    elif words_to_parse[i-1] in n2to9.keys():
        return True, n2to9[words_to_parse[i-1]]
    elif words_to_parse[i-1] in n12to16.keys():
        return True, n12to16[words_to_parse[i-1]]
    elif words_to_parse[i-1] == 'dix':
        if not eof():
            i += 1
            if words_to_parse[i-1] == 'sept':
                return True, 17
            elif words_to_parse[i-1] == 'huit':
                return True, 18
            elif words_to_parse[i-1] == 'neuf':
                return True, 19
        return True, 10
    else:
        i -= 1
        return False, 0

#END
        
        
assert parse_number ("douze") == 12
assert parse_number ("mille douze") == 1012
assert parse_number ("deux million nonante mille trois cent douze") == 2090312
assert parse_number ("huit mille sept cent vingt et un virgule trente et un") == 8721.31
