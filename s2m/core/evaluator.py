class Evaluator:

    def __call__(self, formula, context_formula=None, placeholder_id=1):
        #outputs a score for formula based on a tensorflow calculation
        #TEMPORARY workaround
        if context_formula:
            context_formula.replace_placeholder(formula, placeholder_id, conservative=True)
        else:
            context_formula = formula
        count_brackets_v = self.h_count_brackets(context_formula)[0]
        symmetry = self.h_symmetry(context_formula)
        WEIGHTS = (0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625, 0.0078125, 0.00390625)
        symmetry_v = sum(s * w for s, w in zip(symmetry, WEIGHTS))
        result = (count_brackets_v + symmetry_v) / 2
        return result
    
    ##Functions starting with h_ are heuristics

    #Formula -> [0,1]²
    def h_count_brackets(self, formula):

        y, n = formula.count_brackets()
        s = y + n
        return (y / s,) if s else (1.,)

    #Formula
    def h_symmetry(self, formula):
        
        return tuple([e or 0. for e in formula.d_symmetry()])

evaluator = Evaluator()
