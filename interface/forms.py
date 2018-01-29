from django import forms

from . import models


def validate_email(instance):
    email = instance.cleaned_data['email']
    if models.Utilisateur.objects.filter(email=email):
        raise forms.ValidationError(
            "Cette adresse email possède déjà un compte")
    return email


class InscriptionForm(forms.Form):
    username = forms.CharField(max_length=150, label="Nom d'utilisateur")
    password = forms.CharField(
        widget=forms.PasswordInput, label="Mot de passe")
    password_confirm = forms.CharField(
        widget=forms.PasswordInput, label="Confirmation mot de passe")
    email = forms.EmailField(label="Votre adresse email")

    def clean(self):
        cleaned_data = super(InscriptionForm, self).clean()
        psw_c = self.cleaned_data.get('password_confirm')
        psw = self.cleaned_data.get('password')
        if psw and psw_c:
            if psw != psw_c:
                self.add_error("password_confirm",
                               "Mots de passe non identiques")
        return cleaned_data

    def clean_email(self):
        return validate_email(self)

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) <= 6:
            raise forms.ValidationError(
                "Veuillez entrer un mot de passe de plus de six caractères")
        return password

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) <= 4:
            raise forms.ValidationError(
                "Veuillez entrer un nom d'utilisateur comportant plus de cinq caractères")
        if models.Utilisateur.objects.filter(username=username):
            raise forms.ValidationError("Nom d'utilisateur indisponible")
        return username


class ChangeEmailForm (forms.Form):
    email = forms.EmailField(label="Adresse email")

    def clean_email(self):
        return validate_email(self)


class DeleteAccountForm (forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput, label="Mot de passe")

    def __init__(self, user, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.user = user

    def clean_password(self):
        password = self.cleaned_data['password']
        if not self.user.check_password(password):
            raise forms.ValidationError("Mot de passe incorrect")
        return password


class ChangePasswordForm (forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput, label="Mot de passe")
    new_password = forms.CharField(
        widget=forms.PasswordInput, label="Nouveau mot de passe")
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, label="Confirmer mot de passe")

    def __init__(self, user, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        psw_c = self.cleaned_data.get('confirm_password')
        psw = self.cleaned_data.get('new_password')
        if psw and psw_c:
            if psw != psw_c:
                self.add_error("confirm_password",
                               "Mots de passe non identiques")
        return cleaned_data

    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Mot de passe incorrect")
        return old_password
