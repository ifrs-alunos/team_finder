from tinder.models.base import *
from django.utils.translation import gettext as _
from django.utils import timezone
#with tinder.models.skills as batata

class Group(BaseModel):
	"""docstring for Group"""
	name = models.CharField(max_length=100)
	foundation = models.DateField(_("Foundation Date"), auto_now_add=True)
