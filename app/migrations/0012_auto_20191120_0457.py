# Generated by Django 2.2.7 on 2019-11-20 04:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20191120_0450'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='downvotes',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='upvotes',
        ),
        migrations.RemoveField(
            model_name='post',
            name='downvotes',
        ),
        migrations.RemoveField(
            model_name='post',
            name='upvotes',
        ),
        migrations.DeleteModel(
            name='Vote',
        ),
    ]
