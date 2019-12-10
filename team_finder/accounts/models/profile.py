from django.db import models
from django.core.validators import FileExtensionValidator
from tinder.models import Skill, SkillLevel


def get_avatar_upload(instance, filename):
    return "{}/avatar.jpg".format(instance.owner.username)


class Profile(models.Model):
    owner = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    shortbio = models.TextField(blank=True)
    skills = models.ManyToManyField(Skill, through=SkillLevel, related_name='profiles')

    def __str__(self):
        return self.owner.get_full_name() or self.owner.username

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"

    def set_skill(self, newskill, level):
        new_skill = SkillLevel(profile = self, skill = newskill, level = level)
        new_skill.save()

    def rm_skill(self, skill):
        self.skills.delete(skill)

    def get_skills(self):
        return self.skills.all()


