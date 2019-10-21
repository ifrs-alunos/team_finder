from tinder.models.base import *
from django.utils import timezone


class Group(BaseModel):
	"""docstring for Group"""
	name = models.CharField(max_length=100)
	foundation = models.DateField(auto_now_add=True)
	members = models.ManyToManyField('accounts.Profile', related_name='group_list')
	leader = models.ForeignKey('accounts.Profile', related_name='leader', on_delete=models.SET_NULL, null=True)
	private = models.BooleanField(default=False, help_text='Is this group hidden from others?')

	def __str__(self):
		return("{} -({})".format(self.name, self.foundation))

	def add_member(self, member):
		self.members.add(member)
		self.save()

	def remove_member(self, member):
		self.members.remove(member)
		self.save()
