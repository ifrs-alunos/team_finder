from django.contrib import admin
from .models import Profile
from tinder.models import SkillLevel


class SkillLevelTabular(admin.TabularInline):
    model = SkillLevel
    extra = 0


class ProfileAdmin(admin.ModelAdmin):
    inlines = (SkillLevelTabular, )


admin.site.register(Profile, ProfileAdmin)
# Register your models here.
