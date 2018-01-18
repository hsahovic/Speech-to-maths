class PrefixDict:

    def __init__(self, d={}):
        self.__dict = {}
        self.__reverse_dict = {}
        self.__minlen = float('inf')
        for k, v in d.items():
            self[k] = v

    ##Temp
    def _asDict(self):
        return self.__dict

    def _asReverseDict(self):
        return self.__reverse_dict
    ##End-Temp
    
    def __len__(self):
        return self.__minlen
    
    @classmethod
    def leaves(cls, node, l):
        for k, v in node.items():
            if k is None:
                l.append(v)
            else:
                PrefixDict.leaves(v, l)
        return l

    def children(self, key):
        d = self.__dict
        for c in key:
            if c in d:
                d = d[c]
            else:
                return []
        return [k for k in d.keys() if k is not None]
    
    def get_all(self, key):
        d = self.__dict
        for c in key:
            if c in d:
                d = d[c]
            else:
                return []
        return sorted(PrefixDict.leaves(d, []))

    def get_reverse(self, value):
        if value in self.__reverse_dict:
            return self.__reverse_dict[value]
        else:
            raise KeyError(value)
        
    def __getitem__(self, key):
        d = self.__dict
        for c in key:
            if c in d:
                d = d[c]
            else:
                raise KeyError(key)
        if None in d:
            return d[None]
        else:
            raise KeyError(key)

    def __setitem__(self, key, value):
        d = self.__dict
        for c in key:
            if c in d:
                d = d[c]
            else:
                d[c] = {}
                d = d[c]
        d[None] = value
        if value in self.__reverse_dict:
            self.__reverse_dict[value].add(key)
        else:
            self.__reverse_dict[value] = {key}
        if len(key) < self.__minlen:
            self.__minlen = len(key)

    @classmethod
    def _comp_minlen(cls, d):
        current_min = 0 if None in d else float('inf')
        for key, value in d.items():
            if key is not None:
                current_min = min(current_min,
                                  1 + PrefixDict._comp_minlen(value))
        return current_min
        
    @classmethod
    def _delitem(cls, d, key, i=0):
        if i == len(key):
            del d[None]
        else:
            e = d[key[i]]
            PrefixDict._delitem(e, key, i+1)
            if e == {}:
                del d[key[i]]
        
    def __delitem__(self, key):
        value = self[key]
        if key in self:
            PrefixDict._delitem(self.__dict, key)
        else:
            raise KeyError(key)
        self.__reverse_dict[value].remove(key)
        if not self.__reverse_dict[value]:
            del self.__reverse_dict[value]
        if len(key) == self.__minlen:
            self.__minlen = PrefixDict._comp_minlen(self.__dict)
 
    def __contains__(self, item):
        d = self.__dict
        for c in item:
            if c in d:
                d = d[c]
            else:
                return False
        return None in d
