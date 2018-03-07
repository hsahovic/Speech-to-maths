from math import ceil
from queue import Queue

from s2m.core.prefix_dict import PrefixDict
from s2m.core.phone_string import PhoneString
from s2m.core.phones_map import PhonesMap
from s2m.core.bwoq import BoundedWriteOnlyQueue
from s2m.core.utils import _issilence

class ProximityDict(PrefixDict, PhonesMap):

    INFTY = float('inf')
    __memo = {}
    __memodc = {}
    __memosil = {}

    def _update_cost_pref(self, current_cost, current_prefs, current_min_cost, new_pref):
        if current_cost <= current_min_cost + self.MARGIN:
            if new_pref not in current_prefs \
               or current_prefs[new_pref] > current_cost:
                current_prefs[new_pref] = current_cost
            if current_cost < current_min_cost:
                current_min_cost = current_cost
        return current_min_cost

    def load(self, filename, map=None):
        self.__dict = {}
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                line = line[:-1]
                key, value = line.split(' ', 1)
                key = key.split('(', 1)[0]
                self[PhoneString(value)] = key
        if map:
            self.load_map(map)

    def word_delete_cost(self, word):
        if _issilence(word):
            return 0.
        if word in self.__memodc:
            return self.__memodc[word]
        pronunciations = self.get_reverse(word)
        current_min = self.INFTY
        for pronunciation in pronunciations:
            current_min = min(sum([self.delete_cost(phone) for phone in pronunciation]),
                              current_min)
        return current_min
        
    def find_nearest(self, word, max_count=10):
        if _issilence(word):
            return []
        if word in self.__memo:
            return self.__memo[word]
        pronunciations = self.get_reverse(word)
        nearest = {}
        current_min = self.INFTY
        for pronunciation in pronunciations:
            for nword, score in self.find_nearest_by_pronunciation(pronunciation):
                if nword == word:
                    continue
                if nword in nearest:
                    nearest[nword] = min(nearest[nword],
                                         score)
                else:
                    nearest[nword] = score
                if score < current_min:
                    current_min = score
        output = sorted([(w, s) for w, s in nearest.items()
                         if s <= current_min + self.MARGIN],
                        key=lambda x:x[1])[:max_count]
        self.__memo[word] = output
        return output

    #à supprimer ?

    def _find_nearest_to_silence(self, queue, node, base_cost=0):
        if queue.will_be_rejected(base_cost):
            return
        if node in self:
            queue[self[node]] = base_cost
        for syll in self.children(node):
            new_node = node + PhoneString(syll)
            new_cost = base_cost + self.delete_cost(syll)
            self._find_nearest_to_silence(queue, new_node, new_cost)

    def find_nearest_to_silence(self, max_count=30):
        if self.__memosil:
            return self.__memosil 
        queue = BoundedWriteOnlyQueue(size=max_count)
        self._find_nearest_to_silence(queue, PhoneString(''))
        nearest = {a: b for (a,b) in queue.sorted_list()}
        self.__memosil = nearest
        return nearest

    # à supprimer ? fin -> supprimer aussi le __memosil

    def find_nearest_by_pronunciation(self, word):
        word = PhoneString(word)
        h_len = len(word) + 1
        v_len = max(ceil(self.MAX_LENGTH_FACTOR * len(word)),
                    len(self)) + 1
        #Le tableau créé a toujours plus de lignes que de colonnes
        #On ne maintient qu'une ligne et une colonne à la fois
        #en suivant la diagonale descendante pour remplir la table
        h_nearest = [{} for _ in range(h_len)]
        v_nearest = [{} for _ in range(v_len-1)]
        h_nearest[0] = {PhoneString(''): 0}
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
                        new_pref = pref + PhoneString(next_syll)
                        current_min_cost = self._update_cost_pref(current_cost, current_prefs,
                                                                  current_min_cost, new_pref)
                #Calcul de la distance obtenue par suppression du dernier élément
                if k < h_len-1:
                    for pref, cost in h_nearest[k-j+1].items():
                        for next_syll in self.children(pref):
                            current_cost = self.delete_cost(next_syll) + cost
                            new_pref = pref + PhoneString(next_syll)
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
            for k in range(j+1, v_len):
                current_min_cost = self.INFTY
                current_prefs = {}
                #Calcul de la distance obtenue par remplacement du dernier élément
                for pref, cost in v_nearest[k-j-1].items():
                    for next_syll in self.children(pref):
                        current_replace_cost = self.replace_cost(next_syll, word[j-1])
                        current_cost = current_replace_cost + cost
                        new_pref = pref + PhoneString(next_syll)
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
                        new_pref = pref + PhoneString(next_syll)
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
