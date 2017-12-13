class PlaceHolder(Formula):

    def __init__(self):
        super.__init__(self)

    def __eq__(self, other):
        if other and isinstance(other, PlaceHolder):
            return True
        return False

    def __hash__(self):
        return hash(self)

    def _latex(self):
        return "\\square", 0

    def latex(self):
        return self._latex()[0]

    def count_brackets(self):
       return 0, 0
