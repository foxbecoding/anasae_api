# Generated by Django 4.2.2 on 2023-09-28 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_remove_product_group_id_remove_product_isbn_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productlisting',
            name='title',
            field=models.CharField(default='', max_length=90),
        ),
    ]
