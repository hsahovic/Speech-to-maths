from numpy import log10, ceil
from decimal import Decimal
import re

def natural_log(x) :
    return int(log10(x))

def _set_words(words) : 
    if type(words) == list : 
        for el in words : 
            if type(el) != str : 
                raise ValueError ("Incorrect value for Number Parser. Argument must be of type str or list of str") 
        return words
    elif type(words) == str : 
        return words.split(' ') 
    else : 
        raise ValueError("Incorrect value for Number Parser. Argument must be of type str or list of str")

def listset(l):
    if len(l) < 2:
        return l
    else:
        i = 1
        L = len(l)
        while i < L:
            if l[i] == l[i-1]:
                del l[i]
                L -= 1
            else:
                i += 1
        return l
            
def nobrackets(s):
    bracketted_regex = re.compile(r'\([\w-]+\)', re.UNICODE)
    return bracketted_regex.sub('', s)

def reverse_dict(d):
    e = {}
    for k,y in d.items():
        e[y] = k
    return e

def dec(x):
    return Decimal(str(x))

def args_from_dict(d):
    return reduce(lambda x,y: '%s -%s %s' % (x, y[0], y[1]),
                  d.items())
