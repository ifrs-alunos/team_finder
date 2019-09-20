#IMPORTS

class Othability(object):
	"""docstring for Othability"""
	hability = models.ForeignKey('accounts.Roothability')
	person = models.ForeignKey('accounts.Profile') #accounts.profile substitui o import
		
	def __str__():
		return "{}".format(self.hability, self.person)



