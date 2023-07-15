# Generated by Django 4.0.4 on 2023-07-14 23:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_alter_product_title_alter_productspecification_label_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productspecification',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specifications', to='products.product'),
        ),
    ]