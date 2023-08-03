# Generated by Django 4.2.2 on 2023-08-03 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_userpaymentmethod'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username_validation',
            field=models.CharField(default='', max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='display_name',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(default='', max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(default='', max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='full_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='phone_number',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='usergender',
            name='gender',
            field=models.CharField(max_length=6),
        ),
    ]