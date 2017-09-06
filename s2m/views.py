from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse

import os
import speech_recognition as sr


@login_required
def voice_analysis(request):
    filename = os.path.join("s2m", "file_analysis", "file.wav")
    with open(filename, "wb+") as f:
        for chunk in request.FILES['file'].chunks():
            f.write(chunk)
    return (HttpResponse("Le silence éternel de ces espaces infinis m'effraie."))
