from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse

import os, json
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
    try:
        text = sphinx.to_text(filename_wav)
        print(text)
        parses = s2m_parser(text)
        print(parses)
        response = json.dumps({'instruction': 'WRITE', 'content': parses})
        return (HttpResponse(response))
    except:
        print('boum')
        return (HttpResponse(''))
