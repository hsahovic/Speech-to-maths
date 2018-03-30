from s2m.core.utils import generate_random_word
from interface.models import PendingFormulae

import pickle

def append_formulae(formulae, document):
    formulae_db = PendingFormulae.objects.create(token=generate_random_word(),
                                                 formulae=formulae,
                                                 document=document)
    formulae_db.save()
    print('appended')
    return formulae_db.token
