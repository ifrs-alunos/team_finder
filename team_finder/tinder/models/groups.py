from tinder.models.base import *
from django.utils.translation import gettext as _
from django.utils import timezone
#with tinder.models.skills as batata

class Group(BaseModel):
	"""docstring for Group"""
	name = models.CharField(max_length=100)
	foundation = models.DateField(_("Foundation Date"), auto_now_add=True)
	members = models.ManyToManyField('accounts.Profile', related_name='group_list')
	leader = models.ForeignKey('accounts.Profile', related_name='leader', on_delete=models.SET_NULL, null=True)
	private = models.BooleanField(default=False, help_text='Is this group hidden from others?')

	def __str__(self):
		return("{} -({})".format(self.name, self.foundation))

	def add_member(self, member):
		self.members.add(member)

	def rm_member(self, member):
		self.members.delete(member)

