from threading import Thread
from queue import PriorityQueue
from threading import Condition
from time import time

import json

from tensorflow import Session, Graph
from keras.backend import set_session

from s2m.core.utils import print_important
from s2m.core.S2MParser import s2m_parser
from interface.models import Document

class ParsingQueue(Thread):

    NOP = json.dumps({'instruction': 'nop'})

    def __init__(self):
        self.__queue = PriorityQueue()
        self.__times = {}
        self.__results = {}
        self.__conditions = {}
        Thread.__init__(self)

    def retrieve(self, document):
        _id = document.id
        if _id not in self.__conditions:
            raise ValueError('No result can be retrieved for document %r'
                             % document)
        self.__conditions[_id].acquire()
        try:
            if _id in self.__results:
                result = self.__results.pop(_id)
                return result
            else:
                return self.NOP
        finally:
            self.__conditions[_id].release()

    def schedule(self, text, document, **kwargs):
        _id = document.id
        if _id not in self.__conditions:
            self.__conditions[_id] = Condition()
        condition = self.__conditions[_id]
        self.__queue.put( (time(),
                           _id,
                           text,
                           json.dumps(kwargs)) )
        return condition

    def parse(self, text, sess, document, **kwargs):
        parses = s2m_parser(text, sess, document, **kwargs)
        if not parses or parses[0] == 0:
            for ithbest in nbest:
                parses = s2m_parser(ithbest, sess, document, **kwargs)
                if parses and parses[0] != []:
                    break
        if not parses or parses[0] == []:
            response = json.dumps({'instruction': 'nop'})
        else:
            parses, token = parses
            parses_content, parses_scores = zip(*parses)
            response = json.dumps(
                {'instruction': 'propose', 'content': parses_content, 'scores': parses_scores, 'token': token})
        return response

    def run(self):
        print_important("Info! Thread parsing_queue started.")
        with Session(graph=Graph()) as sess:
            set_session(sess)
            while True:
                action = self.__queue.get()
                _, document_id, text, kwargs = action
                document = Document.objects.get(id=document_id)
                try:
                    response = self.parse(text, sess, document, **json.loads(kwargs))
                except Exception as e:
                    print("Warning! While parsing %r for document %r" \
                          ", the following exception was raised: %r"
                          % (text, document, e))
                    response = self.NOP
                condition = self.__conditions[document_id]
                condition.acquire()
                try:
                    self.__results[document_id] = response
                    condition.notify()
                finally:
                    condition.release()
            
parsing_queue = ParsingQueue()
parsing_queue.start()
