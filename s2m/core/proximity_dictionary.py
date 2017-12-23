from math import ceil

class PrefixDict:

    __dict = {}

    def __init__(self, d={}):
        for k, v in d.items():
            self[k] = v

    @classmethod
    def leaves(cls, node, l):
        for k, v in node.items():
            if k is None:
                l.append(v)
            else:
                PrefixDict.leaves(v, l)
        return l

    def children(self, key):
        if type(key) != str:
            raise TypeError('PrefixDict except keys of type str, not %r'
                            % type(key))
        d = self.__dict
        for c in key:
            if c in d:
                d = d[c]
            else:
                return []
        return [k for k in d.keys() if k is not None]
    
    def get_all(self, key):
        if type(key) != str:
            raise TypeError('PrefixDict except keys of type str, not %r'
                            % type(key))
        d = self.__dict
        for c in key:
            if c in d:
                d = d[c]
            else:
                return []
        return sorted(PrefixDict.leaves(d, []))
    
    def __getitem__(self, key):
        if type(key) != str:
            raise TypeError('PrefixDict except keys of type str, not %r'
                            % type(key))
        d = self.__dict
        for c in key:
            if c in d:
                d = d[c]
            else:
                return KeyError(key)
        if None in d:
            return d[None]
        else:
            return KeyError(key)

    def __setitem__(self, key, value):
        if type(key) != str:
            raise TypeError('PrefixDict except keys of type str, not %r'
                            % type(key))
        d = self.__dict
        for c in key:
            if c in d:
                d = d[c]
            else:
                d[c] = {}
                d = d[c]
        d[None] = value

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
        if type(key) != str:
            raise TypeError('PrefixDict except keys of type str, not %r'
                            % type(key))
        if key in self:
            PrefixDict._delitem(self.__dict, key)
        else:
            raise KeyError(key)
 
    def __contains__(self, item):
        d = self.__dict
        for c in item:
            if c in d:
                d = d[c]
            else:
                return False
        return None in d

class ProximityDict(PrefixDict):

    INFTY = float('inf')
    DELETE_COST = 1
    INSERT_COST = 1
    REPLACE_COST = 1
    MARGIN = 1

    MAX_LENGTH_FACTOR = (INSERT_COST + DELETE_COST) / DELETE_COST

    def insert_cost(self, syll):
        return self.INSERT_COST
    
    def delete_cost(self, syll):
        return self.DELETE_COST
    
    def replace_cost(self, syll1, syll2):
        return 0 if syll1 == syll2 else self.REPLACE_COST

    def _update_cost_pref(self, current_cost, current_prefs, current_min_cost, new_pref):
        if current_cost <= current_min_cost + self.MARGIN:
            if new_pref not in current_prefs \
               or current_prefs[new_pref] > current_cost:
                current_prefs[new_pref] = current_cost
            if current_cost < current_min_cost:
                current_min_cost = current_cost
        return current_min_cost

    def find_nearest(self, word):
        h_len = len(word) + 1
        v_len = ceil(self.MAX_LENGTH_FACTOR * len(word)) + 1
        #Le tableau créé a toujours plus de lignes que de colonnes
        #On ne maintient qu'une ligne et une colonne à la fois
        #en suivant la diagonale descendante pour remplir la table
        h_nearest = [{} for _ in range(h_len)]
        v_nearest = [{} for _ in range(v_len-1)]
        h_nearest[0] = {'': 0}
        for j in range(h_len):
            #Traitement d'une ligne horizontale partant de la position j,j
            for k in range(j or 1, h_len):
                current_min_cost = self.INFTY
                current_prefs = {}
                #Calcul de la distance obtenue par remplacement du dernier élément
                for pref, cost in h_nearest[k-j].items():
                    for next_syll in self.children(pref):
                        current_replace_cost = self.replace_cost(next_syll, word[k-1])
                        current_cost = current_replace_cost + cost
                        new_pref = pref + next_syll
                        current_min_cost = self._update_cost_pref(current_cost, current_prefs,
                                                                  current_min_cost, new_pref)
                #Calcul de la distance obtenue par suppression du dernier élément
                if k < h_len-1:
                    for pref, cost in h_nearest[k-j+1].items():
                        for next_syll in self.children(pref):
                            current_cost = self.delete_cost(next_syll) + cost
                            new_pref = pref + next_syll
                            current_min_cost = self._update_cost_pref(current_cost, current_prefs,
                                                                      current_min_cost, new_pref)
                #Calcul de la distance obtenue par insertion du dernier élément
                if k > j:
                    iter_items = h_nearest[k-j-1].items()
                else:
                    iter_items = v_nearest[0].items()
                for pref, cost in iter_items:
                    current_cost = self.insert_cost(word[k-1]) + cost
                    current_min_cost = self._update_cost_pref(current_cost, current_prefs,
                                                              current_min_cost, pref)
                #Suppression des éléments au-dessus du palier
                h_nearest[k-j] = {}
                for pref, cost in current_prefs.items():
                    if cost <= current_min_cost + self.MARGIN:
                        h_nearest[k-j][pref] = cost
            #Traitement d'une ligne verticale partant de la position j,j
            for k in range(j+1, v_len-1):
                current_min_cost = self.INFTY
                current_prefs = {}
                #Calcul de la distance obtenue par remplacement du dernier élément
                for pref, cost in v_nearest[k-j-1].items():
                    for next_syll in self.children(pref):
                        current_replace_cost = self.replace_cost(next_syll, word[j-1])
                        current_cost = current_replace_cost + cost
                        new_pref = pref + next_syll
                        current_min_cost = self._update_cost_pref(current_cost, current_prefs,
                                                                  current_min_cost, new_pref)
                #Calcul de la distance obtenue par suppression du dernier élément
                if k > j+1:
                    iter_items = v_nearest[k-j-2].items()
                else:
                    iter_items = h_nearest[0].items()
                for pref, cost in iter_items:
                    for next_syll in self.children(pref):
                        current_cost = self.delete_cost(next_syll) + cost
                        new_pref = pref + next_syll
                        current_min_cost = self._update_cost_pref(current_cost, current_prefs,
                                                                  current_min_cost, new_pref)
                        
                #Calcul de la distance obtenue par insertion du dernier élément
                if k-j < v_len-2:
                    for pref, cost in v_nearest[k-j+1].items():
                        current_cost = self.insert_cost(word[j-1]) + cost
                        current_min_cost = self._update_cost_pref(current_cost, current_prefs,
                                                                  current_min_cost, pref)
                #Suppression des éléments au-dessus du palier
                v_nearest[k-j-1] = {}
                for pref, cost in current_prefs.items():
                    if cost <= current_min_cost + self.MARGIN:
                        v_nearest[k-j-1][pref] = cost
        #Génération de l'ensemble final
        nearest = {}
        for hv_nearest in [h_nearest, v_nearest]:
            for dic in hv_nearest:
                for k, v in dic.items():
                    if k in self:
                        if k in nearest:
                            nearest[k] = min(nearest[k], v)
                        else:
                            nearest[k] = v
        #Renvoie la liste des mots les plus proches se trouvant dans le dictionnaire
        return sorted([(self[k], v) for k, v in nearest.items()],
                      key=lambda x:x[1])
        

##Needed
##1. tableau de distance entre les sons
##2. systeme de chargement du dictionnaire
##3. algorithme de calcul de proximity_dictionary (avec sauvegarde)
##4. parser complet
