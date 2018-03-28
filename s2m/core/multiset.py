class Multiset:

    __dict = {}

    def __contains__(self, e):
        return e in __dict

    def __len__(self):
        return sum(self.__dict.values())

    def count(self, e):
        if e in self.__dict:
            return self.__dict[e]
        else:
            return 0

    def add(self, e, count=1):
        if e in self.__dict:
            self.__dict[e] += count
        else:
            self.__dict[e] = count
        
    def remove(self, it):
        if e in self.__dict:
            self.__dict[e] -= 1
            if self.__dict[e] == 0:
                del self.__dict[e]

    def union(self, *argv):
        new_multiset = Multiset(self)
        for e in self:
            new_multiset.add(e, count=self.count(e))
        for other in argv:
            for e in other:
                new_multiset.add(e, count=other.count(e))
        return new_multiset

    def __init__(self, it=None):
        if it:
            if isinstance(it, Multiset):
                for e in it:
                    self.add(e, count=it.count(e))
            else:
                for e in it:
                    self.add(e)
                    
        
            
    
