from s2m.core.formulae import Formula
from s2m.core.utils import merge_lists

class PlaceHolder(Formula):

    PLACEHOLDER_NAMES = ['curseur',
                         'blanc',
                         'un blanc',
                         'quelque chose']

    def __getattr__(self, p):

        if p == 'priority':
            return 5
        else:
            raise AttributeError
        
    def __eq__(self, other):
        if other and isinstance(other, PlaceHolder):
            return True
        return False

    def __hash__(self):
        return hash('PlaceHolder')

    def _latex(self):
        return "\\square", 0

    def latex(self):
        return self._latex()[0]

    def count_brackets(self):
       return 0, 0

    def a_similarity(self, f):
        if isinstance(f, PlaceHolder):
            return 1.
        else:
            return 0

    def d_symmetry(self):
        return merge_lists([], head=1.)

    def transcription(self):
        return 'curseur'

    @classmethod
    def teach(cls, parser):
        parser.add_easy_reduce('placeholder',
                               {x: x for x in cls.PLACEHOLDER_NAMES},
                               lambda _: PlaceHolder(),
                               True)

    @classmethod
    def generate_random(cls):
        return PlaceHolder()
