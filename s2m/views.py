from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse
from django.conf import settings
from django.core.files import File

from interface.models import TrainingSample
from interface.views import get_user

import os
import json

try:
    from s2m.core.S2MParser import s2m_parser
except RuntimeError as e:
    print("Votre code marche pas du coup je l'ignore afin de pouvoir bosser.\nZoubis,\n\nHaris")

from s2m.core.sphinx import sphinx
from s2m.core.utils import wav_from_ogg

def save_and_convert(request, filename_ogg):
    with open(filename_ogg, 'wb+') as f:
        for chunk in request.FILES['file'].chunks():
            f.write(chunk)
    return wav_from_ogg(filename_ogg)

@login_required
def voice_training(request):
    
    #Conversion du fichier ogg en fichier wav
    filename_ogg = os.path.join(settings.MEDIA_ROOT, 'training_data', 'temp.ogg')
    filename_wav = save_and_convert(request, filename_ogg)
    
    #Création d'une nouvelle entrée
    user = get_user(request)
    sample = TrainingSample()
    sample.author = user
    sample.text = 'deux plus deux'
    sample.audio = File(open(filename_wav, 'rb'))
    sample.save()

    #Suppression du fichier wav
    os.remove(filename_wav)

    response = json.dumps({'instruction': 'reload'})
    return (HttpResponse(response))


@login_required
def voice_analysis(request):
    try:
        filename_ogg = os.path.join(settings.MEDIA_ROOT, 'file_analysis', 'file.ogg')
        filename_wav = save_and_convert(request, filename_ogg)
        text, nbest = sphinx.to_text(filename_wav)
        print(text, nbest)
        try:
            parses = s2m_parser(text)
        except:
            parses = []
        if not parses:
            i = 0
            while not parses and i < len(nbest):
                try:
                    parses = s2m_parser(nbest[i])
                except:
                    pass
                i += 1
        response = json.dumps({'instruction': 'write', 'content': parses})
        return (HttpResponse(response))
    except OSError:
        # Windows tests
        return (HttpResponse(json.dumps({'instruction': 'write', 'content': [" Text de test", "T'es de test"]})))
