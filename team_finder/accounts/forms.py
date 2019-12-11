from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class ProfileCreationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ()


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('shortbio', )


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', )

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        widgets = {
            'username': forms.EmailInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'E-mail'
        self.fields['username'].help_text = ""
        self.fields['password1'].label = 'Senha'
        self.fields['password1'].help_text = ''
        self.fields['password2'].label = 'Repita sua senha'
        self.fields['password2'].help_text = ''


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='E-mail', widget=forms.TextInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].label = 'Senha'
