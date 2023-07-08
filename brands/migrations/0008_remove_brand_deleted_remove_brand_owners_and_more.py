# Generated by Django 4.2.2 on 2023-07-08 14:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('brands', '0007_delete_brandowner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brand',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='brand',
            name='owners',
        ),
        migrations.RemoveField(
            model_name='brandlogo',
            name='deleted',
        ),
        migrations.AddField(
            model_name='brand',
            name='creator',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='brands', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='BrandOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.CharField(default='', max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now_add=True, null=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owners', to='brands.brand')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_brands', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]