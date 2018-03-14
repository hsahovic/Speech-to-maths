from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse
from django.conf import settings
from django.core.files import File

import os
import json
import pickle

#Beware! Always load s2m_parser before including sphinx
#so as to make sure config files are generated BEFORE sphinx is turned on
from s2m.core.S2MParser import s2m_parser
# try:
#     from s2m.core.S2MParser import s2m_parser
# except RuntimeError as exc:
#     print("Echec de l'import de s2m_parser dans s2m/views.py ; ignoré par défaut. La reconnaissance vocale échouera.")
# except TypeError as exc :
#     print("Echec de l'import de s2m_parser dans s2m/views.py ; ignoré par défaut. La reconnaissance vocale échouera.")


import s2m.core.sphinx_training

from s2m.core.sphinx import sphinx
from s2m.core.utils import ogg_to_wav
from s2m.settings import MEDIA_ROOT
from interface.models import TrainingSample
from interface.models import PendingFormulae
from interface.models import SavedFormula
from interface.views import get_user
from interface.views_utils import save_file_from_request
from interface.views_utils import get_document


@login_required
def voice_analysis(request):
    try:
        # Chargement du fichier son
        filename_ogg = save_file_from_request(
            request, "ogg", post_arg="file", file_path=os.path.join(MEDIA_ROOT, 'file_analysis'))
        filename_wav = ogg_to_wav(filename_ogg, delete_ogg=True)
        # Chargement de la formule de contexte (si présente)
        context_formula, placeholder_id = None, 0
        if 'context_formula' in request.POST \
           and 'placeholder_id' in request.POST:
            context_formula_id = request.POST['context_formula']
            placeholder_id = request.POST['placeholder_id']
            context_formula_object = SavedFormula.objects.get(id=context_formula_id)
            if context_formula_object:
                context_formula = json.loads(context_formula_object.formula)
        # Conversion du son en texte (Sphinx)
        text, nbest = sphinx.to_text(filename_wav)
        os.remove(filename_wav)
        # Récupération du document
        document = get_document(request)
        # a supprimer une fois le dev fini sur cette sequence
        print(text, nbest)
        # Analyse syntaxique
        try:
            parses = s2m_parser(text,
                                document=document,
                                context_formula=context_formula,
                                placeholder_id=placeholder_id)
        except:
            i = 0
            while not parses and i < len(nbest):
                try:
                    parses = s2m_parser(nbest[i],
                                        document=document,
                                        context_formula=context_formula,
                                        placeholder_id=placeholder_id)
                except:
                    pass
                i += 1
        # Renvoi de la réponse
        if parses == []:
            response = json.dumps({'instruction': 'nop'})
        else:
            parses_content, parses_scores = zip(*parses)
            response = json.dumps({'instruction': 'propose', 'content': parses_content, 'scores': parses_scores})
        return HttpResponse(response)
    except OSError:
        # Windows tests
        return HttpResponse(json.dumps({'instruction': 'propose', 'content': [" Text de test", "T'es de test"]}))


@login_required
def voice_training(request):
    filename_ogg = save_file_from_request(request, "ogg", post_arg="file", file_path=".")
    conversion_bool = False
    filename = filename_ogg
    try:
        filename_wav = ogg_to_wav(filename_ogg)
        filename = filename_wav
        conversion_bool = True
    except OSError:
        pass
    with open(filename, "rb+") as f:
        sample = TrainingSample()
        sample.audio = File(f)
        sample.converted_to_wav = conversion_bool
        sample.author = get_user(request)
        sample.text = request.POST['additionalData']
        sample.save()
    os.remove(filename_wav)
    response = json.dumps({'instruction': 'reload'})
    return HttpResponse(response)


@login_required
def validate_choice(request):
    if not (request.POST \
            and 'token' in request.POST \
            and 'choice' in request.POST):
        raise ValueError('Ill-formatted request passed to validate_choice')
    token = request.POST['token']
    choice = request.POST['choice']
    pending = PendingFormulae.objects.get(token=token)
    if pending:
        formulae = pickle.loads(pending.formulae)
        if choice >= len(formulae):
            raise ValueError
        else:
            for (i, formula) in enumerate(formulae):
                pickled_formula = pickle.dumps(formula)
                saved_formula = SavedFormula.objects.get(formula=pickled_formula)
                if saved_formula:
                    saved_formula.count += 1
                    saved_formula.save()
                    return HttpResponse(saved_formula.id)
                else:
                    formula_db = SavedFormula.objects.create()
                    formula_db.document = pending.document
                    formula_db.formula = pickled_formula
                    formula_db.chosen = (i == choice)
                    formula_db.save()
                    return HttpResponse(formula_db.id)
    else:
        raise ValueError('There are no pending formulae under token %r' % token)

    
@login_required
def help_construction(request):
    print(request.POST['query'])
    response = json.dumps(s2m_parser.help(request.POST['query']))
    return HttpResponse(response)