# Generated by Django 2.2.7 on 2019-12-10 20:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tinder', '0008_auto_20191210_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='leader',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leading', to='accounts.Profile'),
        ),
    ]