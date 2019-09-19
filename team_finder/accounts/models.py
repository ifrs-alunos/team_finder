from django.db import models
from django.core.validators import FileExtensionValidator


def get_avatar_upload(instance, filename):
    return "{}/avatar.jpg".format(instance.owner.username)


class Profile(models.Model):
    owner = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to=get_avatar_upload, 
        validators=[
            FileExtensionValidator(allowed_extensions=['png', 'jpg'])
        ],
    )

    def __str__(self):
        return self.owner.get_full_name() or self.owner.username

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"
