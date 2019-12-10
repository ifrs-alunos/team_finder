from django import forms
from django.core.exceptions import ValidationError

from .models.groups import Group
from accounts.models import Profile


class GroupForm(forms.ModelForm):
	password2 = forms.CharField(
		widget=forms.PasswordInput,
		label='Repita a senha',
		required=False,
	)

	class Meta:
		model = Group
		fields = ('name', 'private', 'password')
		labels = {
			'name': 'Nome',
			'private': 'Privado?',
			'password': 'Senha',
		}

	def clean(self):
		cleaned_data = super(GroupForm, self).clean()
		print(cleaned_data)
		password = cleaned_data['password']
		password2 = cleaned_data['password2']
		private = cleaned_data['private']

		if password != password2:
			self.add_error('password', ValidationError('As senhas devem ser iguais'))

		if private and not password:
			self.add_error('password', ValidationError('Grupos privados devem ter senhas'))

		if not private:
			del cleaned_data['password']
