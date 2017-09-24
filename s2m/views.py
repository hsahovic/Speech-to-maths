from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse

import os
import json
from s2m.core.S2MParser import s2m_parser
from s2m.core.sphinx import sphinx


@login_required
def voice_analysis(request):
    filename_wav = os.path.join("s2m", "file_analysis", "file.wav")
    filename_ogg = os.path.join("s2m", "file_analysis", "file.ogg")
    with open(filename_ogg, "wb+") as f:
        for chunk in request.FILES['file'].chunks():
            f.write(chunk)
    os.system('ffmpeg -y -i "%s" -ar 8000 "%s"' % (filename_ogg, filename_wav))
    os.remove(filename_ogg)
    text, nbest = sphinx.to_text(filename_wav)
    print(text,nbest)
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
#    except:
        # Windows tests
 #       return (HttpResponse(json.dumps({'instruction': 'write', 'content': [" Text de test", "T'es de test"]})))
        # return (HttpResponse(json.dumps({'instruction' : None})))
