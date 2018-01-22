from functools import reduce
from copy import copy

class PhoneString:

    def __init__(self, s):
        if s == '':
            self.__s = []
        elif type(s) is str:
            self.__s = s.split(' ')
        elif type(s) is list:
            self.__s = s
        elif isinstance(s, PhoneString):
            self.__s = list(s)
        else:
            raise TypeError('PhoneString expects str, list or PhoneString, not %r'
                            % type(s))

    def __eq__(self, other):
        return self.__s == list(other)

    def __hash__(self):
        return reduce(lambda a, b: a ^ hash(b), self.__s, 0)

    def __iter__(self):
        return iter(self.__s)
    
    def __list__(self):
        return copy(self.__s)
        
    def __getitem__(self, i):
        return self.__s[i]

    def __repr__(self):
        return ' '.join(self.__s)

    def __len__(self):
        return len(self.__s)

    def __add__(self, other):
        return PhoneString(list(self) + list(other))
