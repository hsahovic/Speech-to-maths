from threading import Thread
from queue import Queue

from tensorflow import Session, Graph
from keras.backend import set_session

from s2m.core.evaluator import evaluator
from s2m.core.utils import print_important
from interface.models import S2MModel

MAX_TRAINING_QUEUE_SIZE = 20


class S2MTraining(Thread):

    def __init__(self):
        self.__queue = Queue(maxsize=MAX_TRAINING_QUEUE_SIZE)
        Thread.__init__(self)

    def enable_system_training(self):
        import s2m.core.system_training_daemon

    def schedule(self, job, no_obj=False, force=False):
        if force:
            self.__queue.put((job, no_obj))
        else:
            try:
                self.__queue.put((job, no_obj), timeout=2)
            except:
                print("Warning! Training task scheduling timeout.")

    def run(self):
        print_important("Info! Thread s2m_training started.")
        with Session(graph=Graph()) as sess:
            set_session(sess)
            system_training_enabled = False
            while True:
                job, no_obj = self.__queue.get()
                if not system_training_enabled:
                    try:
                        self.enable_system_training()
                    except:
                        pass
                    else:
                        system_training_enabled = True
                try:
                    evaluator.train_model(job, sess, no_obj=no_obj)
                except Exception as e:
                    print("Warning! While training S2M model, the following "
                          "exception was raised: " + repr(e))


s2m_training = S2MTraining()
s2m_training.start()
