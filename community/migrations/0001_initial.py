# Generated by Django 4.1.7 on 2025-04-23 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('albums', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='评论内容')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='评论时间')),
            ],
            options={
                'verbose_name': '评论',
                'verbose_name_plural': '评论',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='albums.album', verbose_name='所属相册')),
            ],
            options={
                'verbose_name': '点赞',
                'verbose_name_plural': '点赞',
                'ordering': ['-created_at'],
            },
        ),
    ]
