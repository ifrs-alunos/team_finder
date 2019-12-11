from django import forms
from django.core.exceptions import ValidationError
from accounts.models import Profile

from .models import Group, SkillLevel, Skill
from .fields import ReadOnlySelect


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
		widgets = {
			'password': forms.PasswordInput
		}

	def clean(self):
		cleaned_data = super(GroupForm, self).clean()

		password = cleaned_data['password']
		password2 = cleaned_data['password2']
		private = cleaned_data['private']

		if password != password2:
			self.add_error('password', ValidationError('As senhas devem ser iguais'))

		if private and not password:
			self.add_error('password', ValidationError('Grupos privados devem ter senhas'))

		if not private:
			del cleaned_data['password']


class SkillLevelForm(forms.ModelForm):
	class Meta:
		model = SkillLevel
		fields = ('skill', 'level')

	def __init__(self, *args, **kwargs):
		super(SkillLevelForm, self).__init__(*args, **kwargs)
		self.fields['skill'].disabled = True


def get_skill_level_formset():
	return forms.inlineformset_factory(
		Profile,
		SkillLevel,
		form=SkillLevelForm,
		extra=0,
		max_num=len(SkillLevel.objects.all()),
		can_delete=False,
	)


class PasswordForm(forms.Form):
	password = forms.CharField(widget=forms.PasswordInput, label="Senha de acesso")
