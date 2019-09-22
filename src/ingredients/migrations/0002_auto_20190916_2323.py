# Generated by Django 2.2.5 on 2019-09-16 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredients',
            name='measureUnit',
            field=models.CharField(choices=[('grams', 'g'), ('kilograms', 'kg'), ('centiliter', 'cl'), ('liter', 'l')], max_length=10),
        ),
    ]