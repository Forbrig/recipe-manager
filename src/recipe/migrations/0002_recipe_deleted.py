# Generated by Django 2.2.5 on 2019-09-22 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
