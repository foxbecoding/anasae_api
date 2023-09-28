# Generated by Django 4.2.2 on 2023-09-28 00:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('brands', '0017_alter_brand_bio_alter_brand_name'),
        ('products', '0018_alter_product_description_alter_product_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='group_id',
        ),
        migrations.RemoveField(
            model_name='product',
            name='isbn',
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='stripe_product_id',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.CreateModel(
            name='ProductListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=20, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now_add=True, null=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_listings', to='brands.brand')),
            ],
        ),
        migrations.CreateModel(
            name='ProductDimension',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('length', models.FloatField()),
                ('width', models.FloatField()),
                ('height', models.FloatField()),
                ('weight', models.FloatField()),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now_add=True, null=True)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='dimension', to='products.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='listing',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.productlisting'),
        ),
    ]
