from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse

import os
import speech_recognition as sr

@login_required
def voice_analysis (request) :
#    try :
        filename = os.path.join("s2m", "file_analysis", "file.wav")
        with open(filename, "wb+") as f :
            for chunk in request.FILES['file'].chunks() :
               f.write(chunk)
               
        r = sr.Recognizer()
        with open(filename) as f :

                with sr.AudioFile(f) as source:
                        audio = r.record(source) # read the entire audio file
        # print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
               
#    except : 
#        pass
#    print(':(')
        return (HttpResponse("Le silence éternel de ces espaces infinis m'effraie."))