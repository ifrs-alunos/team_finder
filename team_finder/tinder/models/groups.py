from tinder.models.base import *
from django.utils import timezone


class Group(BaseModel):
	"""docstring for Group"""
	name = models.CharField(max_length=100)
	foundation = models.DateField(auto_now_add=True)
	members = models.ManyToManyField('accounts.Profile', related_name='group_list')
	leader = models.ForeignKey('accounts.Profile', related_name='leader', on_delete=models.SET_NULL, null=True)
	private = models.BooleanField(default=False, help_text='Is this group hidden from others?')
	passwd = models.CharField(max_length=30, null=True)

	def __str__(self):
		return("{} -({})".format(self.name, self.foundation))
