import numpy as np

from django.apps import apps

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

    def evaluate(self, formula, document):
        v_count_brackets = self.h_count_brackets(formula)
        v_symmetry = self.h_symmetry(formula)
        input_vector = np.array(v_count_brackets + v_symmetry)
        user = document.author
        system = apps.get_model('interface', 'S2MModel').objects.get(id=0)
        result_document = self.evaluate_model(document, input_vector)
        result_user = self.evaluate_model(user, input_vector)
        result_system = self.evaluate_model(system, input_vector)
        return (result_document + result_user + result_system) / 3

    def evaluate_model(self, model, document):
        #todo
        return 0.

    def create_empty_model(self):
        #todo
        return None

    def train_model(self, model):
        #todo
        pass
            
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
