# Generated by Django 5.1.1 on 2024-11-11 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voter_analytics', '0003_alter_voter_apartment_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voter',
            name='precinct_number',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='voter',
            name='street_number',
            field=models.TextField(),
        ),
    ]