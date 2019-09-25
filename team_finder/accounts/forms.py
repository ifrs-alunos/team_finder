from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Profile


class ProfileCreationForm(forms.ModelForm):
    first_name = forms.CharField(label="Nome")
    last_name = forms.CharField(label="Sobrenome")
    username = forms.CharField(label="Nome de Usuário")
    email = forms.EmailField(label="E-Mail")
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirme sua senha")

    class Meta:
        model = Profile
        exclude = ('owner', 'avatar',)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('confirm_password', ValidationError('Senhas não são iguais'))

        username = cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            self.add_error('username', ValidationError("E-mail já cadastrado"))

        return cleaned_data

    def save(self, commit=True):
        profile = super(ProfileCreationForm, self).save(commit=False)

        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')

        user = User.objects.create_user(username=username, email=email, password=password,
                                        first_name=first_name, last_name=last_name)
        profile.owner = user

        if commit:
            profile.save()
        return profile


class LoginForm(forms.Form):
    username = forms.EmailField(label='Nome de Usuário')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)


class AvatarChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        widgets = {
            'avatar': forms.FileInput
        }
