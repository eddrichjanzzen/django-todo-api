# Generated by Django 3.1.7 on 2021-02-26 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.TextField(blank=True),
        ),
    ]
