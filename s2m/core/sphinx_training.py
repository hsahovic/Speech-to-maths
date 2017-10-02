import os, re, json
from threading import Thread
from s2m.core.utils import args_from_dict


class SphinxTraining(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):

        #Dossiers
        training_dir = os.path.join("s2m", "training_data")        
        sound_dir = os.path.join(training_dir, "sound")
        text_dir = os.path.join(training_dir, "text")

        sphinx_dir = os.path.join("s2m", "core", "sphinx")
        fr_dir = os.path.join(sphinx_dir, "fr")
        fr_save_dir = os.path.join(sphinx_dir, "fr_save")

        sphinxtrain_dir = os.path.join("/", "usr", "local", "libexec", "sphinxtrain")
        
        #Fichiers
        fileids = os.path.join(training_dir, "s2m.fileids")
        transcription = os.path.join(training_dir, "s2m.transcription")

        mdef = os.path.join(fr_dir, "mdef")
        mdef_txt = os.path.join(fr_dir, "mdef.txt")
        feat_params = os.path.join(fr_dir, "feat.params")

        s2m_dict = os.path.join(sphinx_dir, "s2m.dict")

        bw = os.path.join(sphinxtrain_dir, "bw")
        map_adapt = os.path.join(sphinxtrain_dir, "map_adapt")
        mk_s2sendump = os.path.join(sphinxtrain_dir, "mk_s2sendump")

        #Regex
        ogg_regex = re.compile(r'^(\w+).ogg$', re.UNICODE)
        wav_regex = re.compile(r'^(\w+).wav$', re.UNICODE)
        
        #Conversion des fichiers ogg en fichiers wav
        for _, _, filenames in os.walk(sound_dir):
            for f in filenames:
                ogg = ogg_regex.match(f)
                if ogg:
                    filename_ogg = os.path.join(sound_dir, f)
                    filename_wav = os.path.join(training_dir, ogg.group(1) + '.wav')
                    os.system('ffmpeg -y -i "%s" -ar 8000 "%s"'
                              % (filename_ogg, filename_wav))
                    os.remove(filename_ogg)

        #Extraction des ids et des transcriptions
        with open(fileids, 'w') as i, open(transcription, 'w') as t:
            for _, _, filenames in os.walk(sound_dir):
                for f in filenames:
                    wav = wav_regex.match(f)
                    if wav:
                        i.write(wav.group(1) + '\n')
                        with open(os.join(text_dir, wav.group(1) + '.json')) as j:
                            dic = json.loads(j.read())
                        t.write('<s>%s</s> (%s)\n'
                                % (dic['transcription'], wav.group(1)))

        #Génération des paramètres acoustiques
        fe_params = {'argfile': feat_params,
                     'samprate': '8000',
                     'c': fileids,
                     'di': sound_dir,
                     'do': sound_dir,
                     'ei': 'wav',
                     'eo': 'mfc',
                     'mswav': 'yes'}
        fe_args = args_from_dict(fe_params)
        os.system('sphinx_fe %s' % fe_args)

        #Création de mdef.txt
        os.system('pocketsphinx_mdef_convert -text %s %s'
                  % (mdef, mdef_txt))

        #Collecte des statistiques
        bw_params = {'hmmdir': fr_dir,
                     'moddeffn': mdef_txt,
                     'ts2cbfn': '.ptm.',
                     'feat': '1s_c_d_dd',
                     'svspec': '0-12/13-25/26-38',
                     'cmn': 'current',
                     'agc': 'none',
                     'dictfn': s2m_dict,
                     'ctlfn': fileids,
                     'lsnfn': transcription,
                     'accumdir': training_dir}
        bw_args = args_from_dict(bw_params)
        os.system('%s %s' % (bw, bw_args))

        #Copie
        os.system('cp -a %s %s'
                  % (fr_dir, fr_save_dir))
                  
        
        #Adaptation du modèle (MAP)
        map_adapt_params = {'moddeffn': mdef_txt,
                            'ts2cbfn': '.ptm.',
                            'meanfn': os.path.join(fr_save_dir, 'means'),
                            'varfn': os.path.join(fr_save_dir, 'variances'),
                            'mixwfn': os.path.join(fr_save_dir, 'mixture_weights'),
                            'tmatfn': os.path.join(fr_save_dir, 'transition_matrices'),
                            'accumdir': training_dir,
                            'mapmeanfn': os.path.join(fr_dir, 'means'),
                            'mapvarfn': os.path.join(fr_dir, 'variances'),
                            'mapmixwfn': os.path.join(fr_dir, 'mixture_weights'),
                            'maptmatfn': os.path.join(fr_dir, 'transition_matrices')}
        map_adapt_args = args_from_dict(map_adapt_params)
        os.system('%s %s' % (map_adapt, map_adapt_args))
        
        #Génération du fichier sendump
        mk_s2sendump_params = {'pocketsphinx': 'yes',
                               'moddeffn': mdef_txt,
                               'mixwfn': os.path.join(fr_dir, 'mixture_weights'),
                               'sendumpfn': os.path.join(fr_dir, 'sendump')}

        #Suppression de mdef.txt
        os.remove(mdef_txt)
        
sphinx_training = SphinxTraining()
sphinx_training.start()
