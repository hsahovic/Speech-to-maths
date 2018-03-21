import time

from s2m.core.s2m_training import s2m_training
from s2m.core.utils import print_important
from interface.models import S2MModel

class SystemTrainingDaemon:

    def run(self):
        print_important("Info! Thread system_training_daemon started.") 
        system = S2MModel.objects.get(id=0)
        while True:
            s2m_training.schedule(system, no_obj=True, force=True)
            time.sleep(3600)

system_training_daemon = SystemTrainingDaemon()
