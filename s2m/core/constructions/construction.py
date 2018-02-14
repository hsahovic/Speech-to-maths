from abc import ABCMeta, abstractclassmethod

class Construction(metaclass=ABCMeta):

    @abstractclassmethod
    def generate_help(cls):
        pass

    @classmethod
    def teach(cls, parser):
        for k, v in cls.generate_help().items():
           parser.help_dict[k] = v 
