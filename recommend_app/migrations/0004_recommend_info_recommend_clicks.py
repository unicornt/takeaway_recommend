# Generated by Django 3.1.3 on 2021-04-29 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommend_app', '0003_auto_20210417_2328'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommend_info',
            name='recommend_clicks',
            field=models.IntegerField(default=1, verbose_name='点击数'),
        ),
    ]
