from threading import Thread

import time

from s2m.core.s2m_training import s2m_training
from s2m.core.utils import print_important
from interface.models import S2MModel

class SystemTrainingDaemon(Thread):

    def force(self):
        print("Forcing system training.")
        system = self._system()
        s2m_training.schedule(system, no_obj=True, force=True)
        print("System training forced!")

    def _system(self):
        try:
            system = S2MModel.objects.get(id=0)
            assert not (system.json_model is None
                        or system.weights is None)
        except:
            system = S2MModel.create()
            system.id = 0
            system.save()
        return system
            
    def run(self):
        print_important("Info! Thread system_training_daemon started.")
        system = self._system()
        while True:
            s2m_training.schedule(system, no_obj=True, force=True)
            time.sleep(3600)

system_training_daemon = SystemTrainingDaemon()

system_training_daemon.start()
