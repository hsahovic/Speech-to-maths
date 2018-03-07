from s2m.core.formulae import Formula
from s2m.core.utils import merge_lists

from s2m.core.constructions.placeholder import PlaceHolderConstructions

class PlaceHolder(Formula):

    PLACEHOLDER_NAMES = PlaceHolderConstructions.PLACEHOLDER_NAMES
    PLACEHOLDER_COLORS = PlaceHolderConstructions.PLACEHOLDER_COLORS

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

    def _latex(self, next_placeholder=1, show_id=True):
        if show_id:
            return "\\color{%s}{\\underset{%r}{\\underbrace{\\square}}}" \
                   % (self.PLACEHOLDER_COLORS[next_placeholder % len(self.PLACEHOLDER_COLORS)],
                      next_placeholder), next_placeholder + 1, 0
        else:
            return "\\square", next_placeholder + 1, 0

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

    def replace_placeholder(self, formula, placeholder_id=0, next_placeholder=1):
        return next_placeholder + 1

    @classmethod
    def teach(cls, parser):
        parser.add_easy_reduce('placeholder',
                               {x: x for x in cls.PLACEHOLDER_NAMES},
                               lambda _: PlaceHolder(),
                               True)
        PlaceHolderConstructions.teach(parser)

    @classmethod
    def generate_random(cls):
        return PlaceHolder()
