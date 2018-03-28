from s2m.core.formulae import Formula
from s2m.core.utils import merge_lists
from s2m.core.multiset import Multiset

from s2m.core.constructions.placeholder_constructions import PlaceHolderConstructions

class PlaceHolder(Formula):

    PLACEHOLDER_NAMES = PlaceHolderConstructions.PLACEHOLDER_NAMES
    PLACEHOLDER_COLORS = PlaceHolderConstructions.PLACEHOLDER_COLORS

    def __init__(self):
        self.__b = None

    def __getattr__(self, p):

        if p == 'priority':
            return 5
        elif p == 'b':
            if self.__b:
                return self.__b
            else:
                raise ValueError('PlaceHolder has not been assigned any block yet')
        elif p == 'is_assigned':
            return self.__b is not None
        else:
            raise AttributeError
        
    def __eq__(self, other):
        if other and isinstance(other, PlaceHolder):
            if self.is_assigned:
                return other.is_assigned and self.__b == other.b
            else:
                return not other.is_assigned
        return False

    def __hash__(self):
        if self.is_assigned:
            return hash(self.__b)
        else:
            return hash('PlaceHolder')

    def _latex(self, next_placeholder=1, show_id=True):
        if self.is_assigned:
            a, b, c = self.__b._latex()
            return a, b, c
        else:
            if show_id:
                return "\\color{%s}{\\underset{%r}{\\underbrace{\\square}}}" \
                     % (self.PLACEHOLDER_COLORS[next_placeholder % len(self.PLACEHOLDER_COLORS)],
                        next_placeholder), next_placeholder + 1, 0
            else:
                return "\\square", next_placeholder + 1, 0

    def latex(self):
        return self._latex()[0]

    def count_brackets(self):
        if self.is_assigned:
            return self.__b.count_brackets()
        else:
            return 0, 0
   
    def a_similarity(self, f):
        if self.is_assigned:
            return self.__b.a_similarity(f)
        else:
            if isinstance(f, PlaceHolder):
                return 1.
            else:
                return 0

    def d_symmetry(self):
        if self.is_assigned:
            return self.__b.d_symmetry()
        else:
            return merge_lists([], head=1.)

    def transcription(self):
        if self.is_assigned:
            return self.__b.transcription()
        else:
            return 'curseur'

    def replace_placeholder(self, formula, placeholder_id=0, next_placeholder=1, conservative=False):
        if next_placeholder == placeholder_id \
           and (conservative or not self.is_assigned):
            self.__b = formula
            return 0
        elif not conservative and self.is_assigned:
            return self.__b.replace_placeholder(formula, placeholder_id, next_placeholder, conservative)
        else:
            return next_placeholder + 1

    def tree_depth(self):
        return self.__b.tree_depth() if self.is_assigned else 1

    def extract_3tree(self):
        temp_depth = self.tree_depth()
        if temp_depth == 3:
             return Multiset([self])
        elif temp_depth > 3:
            return self.__b.extract_3tree()
        else:
            return Multiset()

    @classmethod
    def teach(cls, parser):
        parser.add_easy_reduce('placeholder',
                               {x: x for x in cls.PLACEHOLDER_NAMES},
                               lambda _: PlaceHolder(),
                               True,
                               no_pregen=True)
        PlaceHolderConstructions.teach(parser)

    @classmethod
    def generate_random(cls):
        return PlaceHolder()
