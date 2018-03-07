from s2m.core.utils import _unlist

class BoundedWriteOnlyQueue:

    def __init__(self, comparator=None, size=5, args=None):

        self.__size = size
        self.__dict = []
        self.__keys = {}
        self.__ukeys = []
        self.__min = float('inf')
        self.__comparator = comparator or (lambda x, y: x[1] > y[1])
        self.__args = args or ()
        self.__threshold = float('inf')

    def __setitem__(self, key, value):

        ukey = _unlist(key)
        item = key, value

        if self.will_be_rejected(value):
            return

        if value < self.__min:
            self.__min = value
            
        if self.__dict == []:
            self.__dict.append(item)
            self.__ukeys.append(ukey)
            self.__keys[ukey] = 0
            return

        if ukey in self.__keys:
            index = self.__keys[ukey]
            if self.__comparator(self.__dict[index], item, *self.__args):
                self.__dict[index] = item
                self._travel_down(index)
            return

        if len(self.__dict) < self.__size:
            self.__dict.append(item)
            self.__ukeys.append(ukey)
            self.__keys[ukey] = len(self.__dict) - 1
            self._travel_up(len(self.__dict) - 1)

        elif self.__comparator(self.__dict[0], item, *self.__args):
            self._exchange(0, self.__size - 1)
            del self.__keys[self.__ukeys[self.__size - 1]]
            del self.__dict[self.__size - 1]
            del self.__ukeys[self.__size - 1]
            self._travel_down(0)
            self[key] = value

    def __iter__(self):

        return iter(self.__dict)

    def __len__(self):

        return len(self.__dict)

    def clear(self):

        self.__dict = []
        self.__keys = {}
        self.__ukeys = []
        self.__min = float('inf')
    
    def sorted_list(self):

        return sorted(self.__dict, key=lambda x: x[1])

    def prune(self):

        if self.__min == 0:
            while self.__dict[0][1] > 0:
                self._exchange(0, len(self) - 1)
                del self.__dict[-1]
                del self.__keys[self.__ukeys[-1]]
                del self.__ukeys[-1]
                self._travel_down(0)

    def _exchange(self, i, j):

        ukeyi, ukeyj = self.__ukeys[i], self.__ukeys[j]
        self.__keys[ukeyi], self.__keys[ukeyj] = j, i
        self.__dict[i], self.__dict[j] = self.__dict[j], self.__dict[i]
        self.__ukeys[i], self.__ukeys[j] = ukeyj, ukeyi

    def _travel_down(self, i):
	
        if i * 2 >= len(self.__dict):
            return
        elif self.__comparator(self.__dict[i * 2], self.__dict[i], *self.__args):
            if i * 2 + 1 < len(self.__dict) \
            and self.__comparator(self.__dict[i * 2 + 1], self.__dict[i * 2], *self.__args):
                self._exchange(i, i * 2 + 1)
                self._travel_down(i * 2 + 1)
            else:
                self._exchange(i, i * 2)
                self._travel_down(i * 2)
        elif i * 2 + 1 < len(self.__dict) \
        and self.__comparator(self.__dict[i * 2 + 1], self.__dict[i], *self.__args):
            self._exchange(i, i * 2 + 1)
            self._travel_down(i * 2 + 1)

    def _travel_up(self, i):

        if i == 0:
            return
        elif self.__comparator(self.__dict[i], self.__dict[i // 2], *self.__args):
            self._exchange(i, i // 2)
            self._travel_up(i // 2)

    def min_value(self):

        return self.__min

    def set_threshold(self, value):

        self.__threshold = value

    def will_be_rejected(self, value):

        #if len(self.__dict) == self.__size and value > self.__dict[0][1]:
        #    print('len(self.__dict) == self.__size and value > self.__dict[0][1]')
        #elif value > self.__threshold:
        #    print('value > self.__threshold,'+str(self.__threshold)+','+repr(self.sorted_list()))
        #else:
        #    print('niente')
        return (len(self.__dict) == self.__size \
                and value > self.__dict[0][1]) \
               or (value > self.__threshold)
