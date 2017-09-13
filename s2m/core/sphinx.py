import os
from pocketsphinx import Pocketsphinx,AudioFile
class Sphinx:
    def __init__():
        self.config = {
            'verbose': True,
            'hmm': 'sphinx/fr',
            'lm': 'sphinx/fr.lm.dmp',
            'dict': 'sphinx/simple.dict',
            'jsgf': 'sphinx/simple.jsgf',
            }
        self.pocketsphinx=Pocketsphinx(**self.config)    
    def to_text(filename,erase=False):
        loc='s2m/file_analysis' + filename
        text=""
        self.pocketsphinx.decode(audio_file=loc, sampling_rate=8000)
        for s in self.pocketsphinx.segments():
            text+=s+" "
        if erase:
            os.system("bash rm "+loc)
        return text

sphinx = Sphinx()