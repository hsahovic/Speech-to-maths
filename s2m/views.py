from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse
from django.conf import settings
from django.core.files import File

import os
import json

#Beware! Always load s2m_parser before including everything else
#so as to make sure config files are generated BEFORE sphinx is turned on
try:
    from s2m.core.S2MParser import s2m_parser
except RuntimeError as exc:
    print("Echec de l'import de s2m_parser dans s2m/views.py ; ignoré par défaut. La reconnaissance vocale échouera.")


from s2m.core.sphinx import sphinx
from s2m.core.utils import ogg_to_wav
from interface.models import TrainingSample
from interface.views import get_user
from interface.views_utils import save_file_from_request


@login_required
def voice_analysis(request):
    try:
        filename_ogg = save_file_from_request(
            request, "ogg", post_arg="file", file_path=os.path.join(settings.MEDIA_ROOT, 'file_analysis'))
        raise OSError
        filename_wav = ogg_to_wav(filename_ogg, delete_ogg=False)
        # nbest n'est pas lisible, je ne sais pas ce que c'est. Meilleur nom à utiliser.
        text, nbest = sphinx.to_text(filename_wav)
        # a supprimer une fois le dev fini sur cette sequence
        print(text, nbest)
        try:
            parses = s2m_parser(text)
        except:
            parses = []
            # pourquoi cet except s'il amène à renvoyer [] ?
        if not parses:
            i = 0
            while not parses and i < len(nbest):
                try:
                    parses = s2m_parser(nbest[i])
                except:
                    pass
                i += 1
        response = json.dumps({'instruction': 'write', 'content': parses})
        return HttpResponse(response)
    except OSError:
        # Windows tests
        return HttpResponse(json.dumps({'instruction': 'write', 'content': [" Text de test", "T'es de test"]}))


@login_required
def voice_training(request):
    filename_ogg = save_file_from_request(
        request, "ogg", post_arg="file", file_path=os.path.join(settings.MEDIA_ROOT, 'waiting_training_data'))
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
    response = json.dumps({'instruction': 'reload'})
    return HttpResponse(response)
