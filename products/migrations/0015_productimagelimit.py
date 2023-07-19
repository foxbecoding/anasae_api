# Generated by Django 4.2.2 on 2023-07-19 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_alter_productprice_stripe_price_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImageLimit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('limit', models.IntegerField(default=7)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]