from s2m.core.utils import _unlist

class BoundedWriteOnlyQueue:

    def __init__(self, comparator=None, size=5, args=None):

        self.__size = size
        self.__dict = []
        self.__keys = set()
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
            self.__keys.add(ukey)
            return

        if ukey in self.__keys:
            for i in range(len(self.__dict)):
                if self.__dict[i][0] == key:
                    if self.__comparator(self.__dict[i], item, *self.__args):
                        self.__dict[i] = item
                        self._travel_down(i)
                    return

        if len(self.__dict) < self.__size:
            self.__dict.append((key, value))
            self.__keys.add(ukey)
            self._travel_up(len(self.__dict) - 1)

        elif self.__comparator(self.__dict[0], item, *self.__args):

            self.__keys.remove(_unlist(self.__dict[0][0]))
            self.__dict[0] = (key, value)
            self.__keys.add(ukey)
            self._travel_down(0)

    def __iter__(self):

        return iter(self.__dict)

    def __len__(self):

        return len(self.__dict)

    def clear(self):

        self.__dict = []
        self.__keys = set()
        self.__min = float('inf')
    
    def sorted_list(self):

        return sorted(self.__dict, key=lambda x: x[1])

    def prune(self):

        if self.__min == 0:
            new_dict = list(filter(lambda x: x[1] <= self.__min,
                                   self.__dict))
            self.clear()
            for k, v in new_dict:
                self[k] = v

    def _exchange(self, i, j):

        self.__dict[i], self.__dict[j] = self.__dict[j], self.__dict[i]

    def _travel_down(self, i):
	
        if i * 2 >= len(self.__dict):
            return
        elif self.__comparator(self.__dict[i * 2], self.__dict[i], *self.__args):
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

        return (len(self.__dict) == self.__size \
            and value > self.__dict[0][1]) \
            or (value > self.__threshold)
