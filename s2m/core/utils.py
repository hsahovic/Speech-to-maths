from numpy import log10, ceil, sqrt
from decimal import Decimal
from numpy import random
from functools import reduce

import string

import re
import os


def natural_log(x):
    # Doc string ?
    return int(log10(x))


def _set_words(words):
    # Doc string ? Est-ce que ça devrait pas être une méthode du number parser ?
    if type(words) == list:
        for el in words:
            if type(el) != str:
                raise ValueError(
                    "Incorrect value for Number Parser. Argument must be of type str or list of str")
        return words
    elif type(words) == str:
        return words.split(' ')
    else:
        raise ValueError(
            "Incorrect value for Number Parser. Argument must be of type str or list of str")


def listset(l):
    # Doc string ?
    if len(l) < 2:
        return l
    else:
        i = 1
        L = len(l)
        while i < L:
            if l[i] == l[i - 1]:
                del l[i]
                L -= 1
            else:
                i += 1
        return l


def nobrackets(s):
    # Doc string ? + titre pas pep 8 è_é
    bracketted_regex = re.compile(r'\([\w-]+\)', re.UNICODE)
    return bracketted_regex.sub('', s)


def reverse_dict(d):
    # Pourquoi ne pas utiliser return {value : key for key, value in dic} ? Ca serait plus lisible et plus pythonique
    e = {}
    for k, y in d.items():
        e[y] = k
    return e


def dec(x):
    # Doc string ?
    return Decimal(str(x))


def args_from_dict(d):
    # Doc string ?
    return reduce(lambda x, y: '%s -%s %s' % (x, y[0], y[1]),
                  d.items())


def ogg_to_wav(filename_ogg, filename_wav=None, delete_ogg=True):
    """
    Converts ogg file to wav
    If filename_wav is not given, filename_ogg pre-extension content will be used
    """
    filename, extension = os.path.splitext(filename_ogg)
    if extension != '.ogg':
        raise ValueError(
            'An ogg file to be converted to wav must have a valid ogg extension.')
    if filename_wav is None:
        filename_wav = filename + '.wav'
    os.system('ffmpeg -y -i "%s" -ar 8000 "%s"'
              % (filename_ogg, filename_wav))
    if not os.path.exists(filename_wav):
        raise OSError(
            "The conversion didn't work. Make sure ffmpeg works on your system.")
    if delete_ogg:
        os.remove(filename_ogg)
    return filename_wav


def generate_random_word(length=12):
    """
    Returns a str made up of a random sequence of length ascii characters 
    """
    return ''.join(random.choice(list(string.ascii_lowercase)) for i in range(length))


def merge_lists(lists, head=None, length=8):
    l = [] if head is None else [head]
    length = length - 1 if head else length
    lists = [[e for e in l if e is not None] for l in lists]
    if lists == []:
        return l + [None] * length
    n = len(lists)
    lens = [len(l) for l in lists]
    for i in range(max(lens)):
        for j in range(n):
            if i >= lens[j]:
                continue
            else:
                l.append(lists[j][i])
                length -= 1
                if length == 0:
                    return l
    return l + [None] * length


def normalize_scores(liste):
    if liste == []:
        return []
    sum_of_scores = reduce(lambda a,b: a + b[1], liste, 0)
    if sum_of_scores == 0:
        nth = 1 / len(liste)
        return [(a, nth) for a, b in liste]
    else:
        return [(a, b / sum_of_scores) for a, b in liste]


def dist2d(a, b):
    return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)


def norm2d(a):
    return sqrt(a[0]**2 + a[1]**2)
