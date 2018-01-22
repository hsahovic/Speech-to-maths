from interface.models import DocumentConstant
from interface.models import UserConstant
from interface.models import GeneralConstant
from interface.models import Utilisateur
from interface.models import Document

from django.core.exceptions import ObjectDoesNotExist

class ConstantsWrapper():

    def __init__(self, ref):
        if isinstance(ref, Utilisateur) \
           or isinstance(ref, Document):
            self.ref = ref
        else:
            raise ValueError('Reference passed to constants wrapper must be user' \
                             ' or document, not %r' % ref)
        
    def __getattr__(self, name):

        try:
            return self.ref.constset.get(name=name).value
        except ObjectDoesNotExist:
            raise AttributeError('Constant %r not defined for %r' % (name, self.ref))

    def __setattr__(self, name, value):

        if name in self.__dict__ or name == 'ref':
            super().__setattr__(name, value)
        else:
            try:
                entry = self.ref.constset.get(name=name)
                entry.value = value
                entry.save()
            except ObjectDoesNotExist:
                if isinstance(self.ref, Utilisateur):
                    entry = UserConstant(name=name, value=value, user=self.ref)
                elif isinstance(self.ref, Document):
                    entry = DocumentConstant(name=name, value=value, document=self.ref)
                entry.save()

    def __delattr__(self, name):

        try:
            entry = self.ref.constset.get(name=name)
            entry.delete()
        except ObjectDoesNotExist:
            raise AttributeError('Constant %r not defined for %r, cannot delete'
                                 % (name, self.ref))

class GeneralConstants():

    def __getattr__(self, name):

        try:
            return GeneralConstant.objects.get(name=name).value
        except ObjectDoesNotExist:
            raise AttributeError('General constant %r not defined' % name)

    def __setattr__(self, name, value):

        try:
            entry = GeneralConstant.objects.get(name=name)
            entry.value = value
            entry.save()
        except ObjectDoesNotExist:
            entry = GeneralConstant(name=name, value=value)
            entry.save()

    def __delattr__(self, name):

        try:
            entry = GeneralConstant.objects.get(name=name)
            entry.delete()
        except ObjectDoesNotExist:
            raise AttributeError('General constant %r not defined cannot delete' % name)
        
class Constants():

    def user(self, user):

        return ConstantsWrapper(user)

    def document(self, document):

        return ConstantsWrapper(document)

    def general(self):

        return GeneralConstants()

    def create(self, name, value=0.):

        if not GeneralConstant.objects.filter(name=name):
            gc = GeneralConstant(name=name, value=value)
            gc.save()

        for document in Document.objects.all():
            if not document.constset.filter(name=name):
                dc = DocumentConstant(name=name, document=document, value=value)
                dc.save()

        for user in Utilisateur.objects.all():
            if not user.constset.filter(name=name):
                uc = UserConstant(name=name, user=user, value=value)
                uc.save()
                
    def delete(self, name):

        DocumentConstant.objects.filter(name=name).delete()
        UserConstant.objects.filter(name=name).delete()
        GeneralConstant.objects.filter(name=name).delete()

    def create_document_constants(self, document):

        author = document.author
        for constant_name in author.constset.values_list('name', flat=True).distinct():
            uc = author.constset.get(name=constant_name)
            dc = DocumentConstant(name=constant_name, document=document, value=uc.value)
            dc.save()

    def create_user_constants(self, user):

        for constant_name in GeneralConstant.objects.values_list('name', flat=True).distinct():
            gc = GeneralConstant.objects.get(name=constant_name)
            uc = UserConstant(name=constant_name, user=user, value=gc.value)
            uc.save()

            
constants = Constants()
