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
    ff = FFmpeg( inputs={filename_ogg: None},
                 outputs={filename_wav: None} )
    ff.run()
    os.remove(filename_ogg)
    parses = s2m_parser(sphinx.to_text(filename_wav))
    response = json.dumps({'instruction': 'WRITE', 'content': parses})
    return (HttpResponse(response))
