from django.db import models
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

    def set_skills(self, skill_level_set):
        for skill_level in skill_level_set:
            self.add_skill(skill_level.skill, skill_level.level)

    def add_skill(self, skill, level=0):
        new_skill = SkillLevel(profile=self, skill=skill, level=level)
        new_skill.save()

    def rm_skill(self, skill):
        self.skills.delete(skill)

    def has_skill(self, skill):
        return skill in self.skills.all()

    def get_skills(self):
        return self.skills.all()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Profile, self).save(force_insert, force_update, using, update_fields)
        for skill in Skill.objects.all():
            if not self.has_skill(skill):
                self.add_skill(skill)
