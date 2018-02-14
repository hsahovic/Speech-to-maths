from s2m.core.utils import generate_random_word
from interface.models import PendingFormulae

import pickle

def append_formulae(self, formulae, document):
    formulae_db = PendingFormulae.objects.create()
    formulae_db.token = generate_random_word()
    formulae_db.formulae = pickle.dumps(formulae)
    formulae_db.document = document
    formulae_db.save()
