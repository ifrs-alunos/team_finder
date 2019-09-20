#IMPORTS

class Group(object):
	"""docstring for Group"""
	name = models.CharField(max_length=150)
	members = models.ManyToManyField(Profile)
	def __init__(self, arg):
		self.arg = arg

	def __str__():
		return "{}".format()

	
		