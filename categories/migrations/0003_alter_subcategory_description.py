# Generated by Django 4.2.2 on 2023-07-11 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_remove_subcategoryproductspecificationitemoption_subcategory_product_specification_item_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategory',
            name='description',
            field=models.TextField(max_length=2000),
        ),
    ]
