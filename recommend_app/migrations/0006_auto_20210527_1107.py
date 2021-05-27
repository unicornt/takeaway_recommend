# Generated by Django 3.1.3 on 2021-05-27 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommend_app', '0005_recommend_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='recommend_click',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('click_id', models.CharField(max_length=20, verbose_name='点击推荐编号')),
                ('click_user', models.CharField(max_length=20, verbose_name='点击的用户名')),
                ('click_date', models.DateTimeField(auto_now_add=True)),
                ('click_time', models.CharField(default='正餐', max_length=20, verbose_name='推荐时段')),
                ('click_catalog', models.CharField(default='炒菜饭', max_length=20, verbose_name='推荐类别')),
            ],
        ),
        migrations.AddField(
            model_name='recommend_info',
            name='recommend_catalog',
            field=models.CharField(default='炒菜饭', max_length=20, verbose_name='推荐类别'),
        ),
        migrations.AddField(
            model_name='recommend_info',
            name='recommend_time',
            field=models.CharField(default='正餐', max_length=20, verbose_name='推荐时段'),
        ),
        migrations.AddField(
            model_name='recommend_like',
            name='like_catalog',
            field=models.CharField(default='炒菜饭', max_length=20, verbose_name='推荐类别'),
        ),
        migrations.AddField(
            model_name='recommend_like',
            name='like_time',
            field=models.CharField(default='正餐', max_length=20, verbose_name='推荐时段'),
        ),
    ]
