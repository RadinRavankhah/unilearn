# Generated by Django 2.2.7 on 2019-11-14 11:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upvotes', models.IntegerField()),
                ('downvotes', models.IntegerField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=50)),
                ('content', models.TextField()),
                ('upvotes', models.IntegerField()),
                ('downvotes', models.IntegerField()),
                ('created_on', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(blank=True, max_length=200)),
                ('username', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('karma', models.IntegerField(default=0)),
                ('password', models.CharField(max_length=20)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voted', models.BooleanField()),
                ('comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Comment')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Sub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('members', models.ManyToManyField(to='app.UserProfile')),
                ('posts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Post')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='created_by',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.UserProfile'),
        ),
        migrations.AddField(
            model_name='post',
            name='sub_posted_on',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.Sub'),
        ),
        migrations.AddField(
            model_name='comment',
            name='created_by',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.UserProfile'),
        ),
        migrations.AddField(
            model_name='comment',
            name='parent_post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Post'),
        ),
    ]
