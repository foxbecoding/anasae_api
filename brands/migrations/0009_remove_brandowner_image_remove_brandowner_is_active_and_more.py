# Generated by Django 4.2.2 on 2023-07-08 15:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('brands', '0008_remove_brand_deleted_remove_brand_owners_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brandowner',
            name='image',
        ),
        migrations.RemoveField(
            model_name='brandowner',
            name='is_active',
        ),
        migrations.CreateModel(
            name='BrandFollower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now_add=True, null=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='brands.brand')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following_brands', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
