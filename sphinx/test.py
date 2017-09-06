import os
from pocketsphinx import Pocketsphinx

config = {
    'verbose': True,
    'hmm': 'fr',
    'lm': 'fr.lm.dmp',
    'dict': 'simple.dict',
    'jsgf': 'simple.jsgf',
    }

ps = Pocketsphinx(**config)

print('Ready')

while True:
    ps.decode(audio_file=input())
    print(ps.segments())
