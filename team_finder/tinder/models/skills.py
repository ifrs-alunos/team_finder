from tinder.models.base import *

class Skill(models.Model):
	KNAREA = [
		("P","Physical Aptitude"),
		("A","Artistic Skill"),
		("B","Biological Science"),
		("H","Human Science"),
		("E","Exact Science"),
		("S","Social Skill"),
	]
	name = models.CharField(max_length=200)
	area = models.CharField(max_length=1, choices=KNAREA, default='A')

	def __str__(self):
		return("{}".format(self.name))
