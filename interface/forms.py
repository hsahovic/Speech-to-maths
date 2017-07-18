from django import forms

from . import models

class InscriptionForm (forms.Form):
    username = forms.CharField(max_length=150, label = "Nom d'utilisateur")
    password = forms.CharField(widget=forms.PasswordInput, label = "Mot de passe")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label = "Confirmation mot de passe")
    email = forms.EmailField(label="Votre adresse email")
    
    def clean_password (self) :
        password = self.cleaned_data['password']
        if len(password) <= 6 :
            raise forms.ValidationError ("Veuillez entrer un mot de passe de plus de six caractères")
        return password
    
    def clean (self) :
        cleaned_data = super(InscriptionForm, self).clean()
        psw_c = self.cleaned_data.get('password_confirm')
        psw = self.cleaned_data.get('password')
        if psw and psw_c :
            if psw != psw_c :
                self.add_error("password_confirm", "Mots de passe non identiques")
        return cleaned_data
    
    def clean_username (self) :
        username = self.cleaned_data['username']
        if len(username) <= 4 :
            raise forms.ValidationError ("Veuillez entrer un nom d'utilisateur comportant plus de cinq caractères")
        if models.Utilisateur.objects.filter(username = username) :
            raise forms.ValidationError ("Nom d'utilisateur indisponible")
        return username
    
    def clean_email (self) :
        email = self.cleaned_data['email']
        if models.Utilisateur.objects.filter(email = email) :
            raise forms.ValidationError ("Cette adresse email possède déjà un compte")
        return email