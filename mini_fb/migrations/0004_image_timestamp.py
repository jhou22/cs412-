# Generated by Django 5.1.1 on 2024-10-21 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini_fb', '0003_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
