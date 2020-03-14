# Generated by Django 2.2.7 on 2020-03-14 11:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webapp', '0003_file_general_access'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='users_private',
            field=models.ManyToManyField(related_name='file_private', to=settings.AUTH_USER_MODEL, verbose_name='Приват'),
        ),
    ]
