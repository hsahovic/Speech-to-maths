from s2m.core.utils import norm2d, dist2d

class PhonesMap:

    MARGIN = 1.
    MAX_LENGTH_FACTOR = 2.

    def load_map(self, filename):
        self.__map = {}
        maps_max = {}
        with open(filename, 'r', encoding='utf-8') as f:
            current_map = None
            lines = f.readlines()
            for line in lines:
                value, x, y = line.split(' ')
                if value == 'new' and x == 'map':
                    current_map = y
                    maps_max[y] = 0
                else:
                    x, y = float(x), float(y)
                    if not current_map:
                        raise ValueError('Error in file %r, please start ' \
                                         'new map before declaring points'
                                         % filename)
                    else:
                        self.__map[value] = (current_map, x, y)
                        maps_max[current_map] = max(maps_max[current_map],
                                                    norm2d((x, y)))
        for k, v in self.__map.items():
            f = 2 * maps_max[v[0]]
            if f == 0:
                continue
            x, y = v[1] / f, v[2] / f
            self.__map[k] = (v[0], x, y)
    
    def insert_cost(self, phone):
        if phone not in self.__map:
            raise KeyError('Phone %r not in map' % phone)
        return norm2d(self.__map[phone][1:])

    def delete_cost(self, phone):
        return self.insert_cost(phone)

    def replace_cost(self, phone1, phone2):
        m1, x1, y1 = self.__map[phone1]
        m2, x2, y2 = self.__map[phone2]
        if m1 != m2:
            return 1.
        else:
            return dist2d((x1,y1),(x2,y2))
