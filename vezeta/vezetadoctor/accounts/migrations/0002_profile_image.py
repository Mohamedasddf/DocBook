# Generated by Django 3.0 on 2025-01-24 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default_image.jpg', upload_to='images/'),
        ),
    ]
