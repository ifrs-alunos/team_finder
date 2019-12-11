from django import forms
from .models.groups import Group

class GroupForm(forms.ModelForm):
	class Meta:
		model = Group
		fields = '__all__'
		widgets = {
			
		}
