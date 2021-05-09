# Generated by Django 3.1.7 on 2021-05-07 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommend_app', '0004_recommend_info_recommend_clicks'),
    ]

    operations = [
        migrations.CreateModel(
            name='recommend_like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_id', models.CharField(max_length=20, verbose_name='点赞推荐编号')),
                ('like_user', models.CharField(max_length=20, verbose_name='点赞的用户名')),
            ],
        ),
    ]