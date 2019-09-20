#IMPORTS

class Roothability(object):
	"""docstring for Roothability"""
	AREA_CHOICES = [
	("P","Physical Aptitude"),
	("A","Artistic Sciences"),
	("B","Biological Sciences"),
	("H","Human Sciences"),
	("E","Exact Sciences"),
	("S","Social Aptitude"),
]

	name = models.CharField(max_length=200)
	area = models.CharField(choices=AREA_CHOICES, max_length=1)
		
	def __str__():
		return "{}".format(self.name, self.area)
