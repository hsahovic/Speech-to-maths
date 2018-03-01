from s2m.core.constructions.constructions import Construction

class PlaceHolderConstructions(Construction):

    PLACEHOLDER_NAMES = ['curseur',
                         'blanc',
                         'un blanc',
                         'quelque chose']

    PLACEHOLDER_COLORS = ['blue',
                          'red',
                          'orange',
                          'olive',
                          'brown',
                          'darkgray',
                          'purple',
                          'violet']

    @classmethod
    def generate_help(cls):
        help = {}
        for k in cls.PLACEHOLDER_NAMES:
            help[k] = {'name': 'curseur',
                       'latex': '\\square',
                       'spelling': k}
        return help
