# Generated by Django 2.2.7 on 2019-12-10 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tinder', '0006_group_passwd'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='passwd',
        ),
        migrations.AddField(
            model_name='group',
            name='password',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
