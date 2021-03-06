# Generated by Django 3.1.3 on 2021-04-08 11:34

from django.db import migrations, models
import recommend_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='recommend_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recommend_key', models.CharField(max_length=20, unique=True, verbose_name='推荐对应id')),
                ('recommend_user', models.CharField(max_length=20, unique=True, verbose_name='推荐用户')),
                ('recommend_title', models.TextField(max_length=200, verbose_name='推荐标题')),
                ('recommend_text', models.TextField(max_length=10000, verbose_name='推荐文本')),
                ('recommend_piclist', models.CharField(max_length=1000, verbose_name='存储图片列表')),
                ('recommend_flag', models.BooleanField(default=False, verbose_name='信息是否上传')),
                ('recommend_picnum', models.IntegerField(verbose_name='图片数量')),
                ('recommend_like', models.IntegerField(default=0, verbose_name='喜欢数量')),
            ],
        ),
        migrations.CreateModel(
            name='recommend_pic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture_id', models.CharField(max_length=20, unique=True, verbose_name='图片编号(UTC时间)表示存储名')),
                ('picture_key', models.CharField(max_length=20, unique=True, verbose_name='图片对应推荐编号')),
                ('picture', models.ImageField(blank=True, null=True, upload_to=recommend_app.models.recommend_path, verbose_name='推荐图片')),
            ],
        ),
    ]
