# Generated by Django 4.2.2 on 2023-07-08 03:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brands', '0005_rename_owners_brand_owner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='brand',
            old_name='owner',
            new_name='owners',
        ),
    ]