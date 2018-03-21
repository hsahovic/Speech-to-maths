from threading import Thread
from queue import Queue

from s2m.core.evaluator import evaluator
from s2m.core.utils import print_important
from interface.models import S2MModel

class S2MTraining(Thread):

    def __init__(self):
        self.__queue = Queue(maxsize=20)
        Thread.__init__(self)

    def enable_system_training(self):
        system = S2MModel.objects.get(id=0)
        if not system:
            system = S2MModel()
            system.id = 0
            system.json_model = self.create_empty_model()
            system.save()
        import s2m.core.system_training_daemon

    def schedule(self, job, force=False):
        if force:
            self.__queue.put(job)
        else:
            try:
                self.__queue.put(job, timeout=2)
            except:
                print("Warning! Training task scheduling timeout.")

    def run(self):
        print_important("Info! Thread s2m_training started.")
        system_training_enabled = False
        while True:
            job = self.__queue.get()
            if not system_training_enabled:
                try:
                    self.enable_system_training()
                except Exception:
                    pass
                else:
                    system_training_enabled = True
            try:
                evaluator.train_model(job)
            except Exception as e:
                print("Warning! While training S2M model, the following " \
                      "exception was raised: " + repr(e))

s2m_training = S2MTraining()
s2m_training.start()
