# Generated by Django 4.2.2 on 2023-09-04 19:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_userfollower'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPaymentMethodBillingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now_add=True, null=True)),
                ('deleted', models.DateTimeField(null=True)),
                ('address', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='for_payment_methods', to='users.useraddress')),
                ('paymentMethod', models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, related_name='billing_address', to='users.userpaymentmethod')),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='billing_addresses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
