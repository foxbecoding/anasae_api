# Generated by Django 4.2.2 on 2023-10-18 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='uid',
            field=models.CharField(default='', max_length=20, unique=True),
        ),
    ]
