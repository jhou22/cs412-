# Generated by Django 5.1.1 on 2024-11-11 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voter_analytics', '0002_alter_voter_voter_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voter',
            name='apartment_number',
            field=models.TextField(),
        ),
    ]
