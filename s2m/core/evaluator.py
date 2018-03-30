import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.models import model_from_json
from django.apps import apps

import pickle

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
        input_vector = self.h_all(formula)
        user = document.author
        system = apps.get_model('interface', 'S2MModel').objects.get(id=0)
        result_document = self.evaluate_model(document, input_vector)
        result_user = self.evaluate_model(user, input_vector)
        result_system = self.evaluate_model(system, input_vector)
        return (result_document + result_user + result_system) / 3

    def evaluate_model(self, obj, input_vector):
        if len(input_vector.shape) == 1:
            input_vector.shape = (input_vector.shape[0],1)
        if not obj.s2m_model:
            model = apps.get_model('interface', 'S2MModel')()
            model.save()
            obj.s2m_model = model
            obj.save()
        else:
            model = model_from_json(obj.s2m_model)
        return model.predict(input_vector)
        
    def create_empty_model(self):
        model = Sequential()
        model.add(Dense(32, activation='relu', input_dim=9))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])
        return model

    def train_model(self, obj, no_obj=False):
        saved_formulae = apps.get_model('interface', 'SavedFormula').objects.all()
        data, labels = zip([(np.array(self.h_all(f.formula)), float(f.chosen)) for f in saved_formulae])
        np_data, np_labels = np.array(data), np.array(labels)
        if not no_obj and not obj.s2m_model:
            model = apps.get_model('interface', 'S2MModel')()
            model.save()
            obj.s2m_model = model
            obj.save()
        elif no_obj:
            model = obj
        kmodel = model_from_json(model.json_model)
        kmodel.fit(np_data, np_labels, epoch=10, batch_size=32)
        model.json_model = kmodel.to_json()
        model.save()

    def h_all(self, formula):
        v_count_brackets = self.h_count_brackets(formula)
        v_symmetry = self.h_symmetry(formula)
        v_all = np.array(v_count_brackets + v_symmetry)
        return v_all

    ##Functions starting with h_ are heuristics

    def h_count_brackets(self, formula):
        y, n = formula.count_brackets()
        s = y + n
        return (y / s,) if s else (1.,)

    def h_symmetry(self, formula):
        return tuple([e or 0. for e in formula.d_symmetry()])

    def h_3tree(self, formula, obj, length=8):
        #Prendre compte obj
        model = apps.get_model('interface', 'ElementaryFormula')
        elementary_formulae = formula.extract_3tree()
        results = []
        for elementary_formula in elementary_formulae:
            pickled_elementary_formula = pickle.dumps(elementary_formula)
            db_elementary_formula = model.objects.get(formula=pickled_elementary_formula)
            doc_count = elementary_formulae.count(elementary_formula)
            if db_elementary_formula:
                db_count = db_elementary_formula.count
            else:
                db_count = 0
            results.append( (doc_count, 1. - 1. / (1 + db_count)) )
        results.sort(reverse=True)
        return results[:length]
            
    def h_averagesildepth(self, formula):

       depths, counts = formula.count_silsdepths()
       return (depths/counts,) if counts else (0,)

evaluator = Evaluator()
