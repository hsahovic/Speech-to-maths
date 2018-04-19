from s2m.core.utils import generate_random_word
from interface.models import PendingFormulae

import pickle

def append_formulae(formulae, document):
    pickled_formulae = pickle.dumps(formulae)
    formulae_db = PendingFormulae.objects.create(token=generate_random_word(),
                                                 formulae=pickled_formulae,
                                                 document=document)
    formulae_db.save()
    return formulae_db.token
