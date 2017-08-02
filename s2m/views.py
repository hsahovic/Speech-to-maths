from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse

import os

@login_required
def voice_analysis (request) :
    try :
        with open("s2m%sfile_analysis%sfile.ogg" % (os.sep, os.sep), "wb+") as f :
            for chunck in request.FILES['file'].chunks() :
               f.write(chunck)
    except : 
        pass
    return (HttpResponse("Le silence éternel de ces espaces infinis m'effraie."))