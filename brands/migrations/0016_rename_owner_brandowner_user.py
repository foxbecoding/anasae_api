# Generated by Django 4.2.2 on 2023-07-09 20:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brands', '0015_rename_rater_brandrating_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='brandowner',
            old_name='owner',
            new_name='user',
        ),
    ]
