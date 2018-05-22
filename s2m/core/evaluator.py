import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.models import model_from_json
from django.apps import apps

from time import time

import pickle

class Evaluator:

    def __init__(self):

        self.__memo = {}
        self.__memo_eval = {}

    def __call__(self, formula, sess, document, context_formula=None, placeholder_id=1):
        #outputs a score for formula based on a tensorflow calculation
        #TEMPORARY workaround
        if context_formula:
            context_formula.replace_placeholder(formula, placeholder_id, conservative=True)
        else:
            context_formula = formula
        #count_brackets_v = self.h_count_brackets(context_formula)[0]
        #symmetry = self.h_symmetry(context_formula)
        #WEIGHTS = (0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625, 0.0078125, 0.00390625)
        #symmetry_v = sum(s * w for s, w in zip(symmetry, WEIGHTS))
        #result = (count_brackets_v + symmetry_v) / 2
        #return result
        return self.evaluate(formula, sess, document)

    def reset(self):
        self.__memo = {}

    def evaluate(self, formula, sess, document):
        if (formula, sess, document) in self.__memo_eval:
            return self.__memo_eval[(formula, sess, document)]
        input_vector = self.h_all(formula)
        user = document.author
        system = apps.get_model('interface', 'S2MModel').objects.get(id=0)
        result_document = self.evaluate_model(document, sess, input_vector)
        result_user = self.evaluate_model(user, sess, input_vector)
        result_system = self.evaluate_model(system, sess, input_vector)
        result = (result_document + result_user + result_system) / 3
        self.__memo_eval[(formula, sess, document)] = result
        return result

    def _s2m_model_from_obj(self, obj, no_obj=False):
        S2MModel = apps.get_model('interface', 'S2MModel')
        #Premier cas : obj est déjà un S2MModel
        if isinstance(obj, S2MModel):
            s2m_model = obj
        #Deuxième cas : création d'un S2MModel nécessaire
        elif (not no_obj) and (not obj.s2m_model):
            s2m_model = S2MModel.create()
            s2m_model.save()
            obj.s2m_model = s2m_model
            obj.save()
        #Troisième cas : le S2MModel existe déjà
        else:
            s2m_model = obj.s2m_model
        return s2m_model
        
    def evaluate_model(self, obj, sess, input_vector):
        input_vectors = np.array([input_vector])
        kmodel = self._load_s2m_model_from_obj(obj, sess)
        return kmodel.predict(input_vectors)[0][0]
        
    def create_empty_model(self):
        model = Sequential()
        model.add(Dense(32, activation='relu', input_dim=9))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(1, activation='sigmoid'))
        return model

    def _load_s2m_model(self, s2m_model):
        kmodel = model_from_json(s2m_model.json_model)
        kmodel.set_weights(pickle.loads(s2m_model.weights))
        kmodel.compile(optimizer='rmsprop',
                       loss='binary_crossentropy',
                       metrics=['accuracy'])
        return kmodel

    def _load_s2m_model_from_obj(self, obj, sess, no_obj=False):
        if (sess, obj) in self.__memo:
            return self.__memo[(sess, obj)]
        else:
            s2m_model = self._s2m_model_from_obj(obj, no_obj)
            kmodel = self._load_s2m_model(s2m_model)
            self.__memo[(sess, obj)] = kmodel
            return kmodel

    def train_model(self, obj, sess, no_obj=False):
        #Chargement des modèles (depuis apps pour éviter les imports cycliques)
        SavedFormula = apps.get_model('interface', 'SavedFormula')
        #Récupération des données d'apprentissage
        saved_formulae = SavedFormula.objects.all()
        data, labels = zip(*[(np.array(self.h_all(pickle.loads(f.formula))), float(f.chosen)) for f in saved_formulae])
        np_data, np_labels = np.array(data), np.array(labels)
        #Extraction du S2MModel pertinent
        s2m_model = self._s2m_model_from_obj(obj, no_obj)
        #Chargement du model keras
        kmodel = self._load_s2m_model_from_obj(obj, sess, no_obj)
        #Régression
        kmodel.fit(np_data, np_labels, epochs=10, batch_size=32)
        #Sauvegarde des coefficients dans la BDD
        s2m_model.weights = pickle.dumps(kmodel.get_weights())
        s2m_model.save()

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
