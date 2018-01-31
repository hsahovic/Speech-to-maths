import os
from threading import Thread
from pocketsphinx import Pocketsphinx, AudioFile
from s2m.core.utils import nobrackets


class Sphinx(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.ready = False

    def run(self):
        self.config = {
            'verbose': True,
            'hmm': os.path.join('s2m', 'core', 'sphinx', 'fr'),
            'lm': os.path.join('s2m', 'core', 'sphinx', 'fr.lm.dmp'),
            'dict': os.path.join('s2m', 'core', 'sphinx', 's2m.dict'),
            'jsgf': os.path.join('s2m', 'core', 'sphinx', 's2m.jsgf'),
        }
        self.pocketsphinx = Pocketsphinx(**self.config)
        self.ready = True

    def get_silence(self, duration):
        if duration < 0.25:
            return '[veryshortsil]'
        elif duration < 0.5:
            return '[shortsil]'
        elif duration < 1.5:
            return '[sil]'
        elif duration < 3.:
            return '[longsil]'
        else:
            return '[verylongsil]'

    def get_segment_string(self, segments):
        segment_list = []
        last_silence = 0
        spoken_duration = 0
        word_count = 0
        for segment in segments:
            if segment.word in ['<s>', '</s>']:
                continue
            elif segment.word == '<sil>':
                last_silence += segment.end_frame - segment.start_frame
            else:
                if last_silence > 0:
                    segment_list.append(last_silence)
                    last_silence = 0
                spoken_duration += segment.end_frame - segment.start_frame
                segment_list.append(segment.word)
                word_count += 1
        avg_word_duration = spoken_duration / word_count
        return ' '.join((self.get_silence(s / avg_word_duration)
                         if type(s) is int else nobrackets(s))
                        for s in segment_list)
    
    def to_text(self, filename, erase=False):
        if not self.ready:
            raise EnvironmentError('Initialization of sphinx not finished.')
        FILLER_WORDS = ['<s>', '<sil>', '</s>']
        self.pocketsphinx.decode(filename)
        text = " ".join(
           [s for s in self.pocketsphinx.segments() if s not in FILLER_WORDS])
        text = nobrackets(text)
        segment_string = self.get_segment_string(self.pocketsphinx.seg())
        nbest = [nobrackets(w[0])
                 for w in self.pocketsphinx.best(count=10)[1:]]
        if erase:
            os.remove(loc)
        return segment_string, nbest

sphinx = Sphinx()
sphinx.start()
