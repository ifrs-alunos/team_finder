from django.db import models
from django.core.validators import FileExtensionValidator
from tinder.models import Skill, SkillLevel, Group


def get_avatar_upload(instance, filename):
    return "{}/avatar.jpg".format(instance.owner.username)

class Profile(models.Model):
    #Attributes
    owner = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    shortbio = models.TextField(help_text='A short description of the person', default="This user's shortbio hasn't been defined yet.")
    skills = models.ManyToManyField(Skill, through=SkillLevel, related_name='profiles')

    avatar = models.ImageField(
        upload_to=get_avatar_upload, 
        validators=[
            FileExtensionValidator(allowed_extensions=['png', 'jpg'])
        ], 
    )

    #Functions
    def __str__(self):
        return self.owner.get_full_name() or self.owner.username

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"
