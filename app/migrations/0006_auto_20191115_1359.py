# Generated by Django 2.2.7 on 2019-11-15 13:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_comment_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='downvotes',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='comment',
            name='upvotes',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='sub',
            name='members',
            field=models.ManyToManyField(blank=True, to='app.UserProfile'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
