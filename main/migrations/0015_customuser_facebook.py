# Generated by Django 5.1.4 on 2024-12-29 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_rename_bio_customuser_description_customuser_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='facebook',
            field=models.URLField(blank=True, default='http://facebook.com', null=True),
        ),
    ]
