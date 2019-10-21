from tinder.models.base import *

#Skill_Level is serving as through to user and skills
class SkillLevel(BaseModel):
	SKLEVEL = [
		(1, "Ameba"),
		(2, "Vegetal"),
		(3, "Ser Pensante"),
		(4, "Malandrão"),
		(5, "Topzera"),
	]

	profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
	skill = models.ForeignKey('Skill', related_name='levels', on_delete=models.CASCADE)
	level = models.IntegerField(choices=SKLEVEL, default=1)

	def __str__(self):
		return("{} (LVL.{}) - Profile: {}".format(self.profile, self.skill, self.level))