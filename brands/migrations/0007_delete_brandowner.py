# Generated by Django 4.2.2 on 2023-07-08 04:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brands', '0006_rename_owner_brand_owners'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BrandOwner',
        ),
    ]
