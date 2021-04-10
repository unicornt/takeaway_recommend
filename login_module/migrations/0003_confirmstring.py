# Generated by Django 3.1.3 on 2021-04-05 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_module', '0002_auto_20210326_1937'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfirmString',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=256, verbose_name='confirm code')),
                ('usr_email', models.EmailField(max_length=254, null=True, unique=True, verbose_name='用户邮箱')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Confirm Code',
                'verbose_name_plural': 'Confirm Codes',
                'ordering': ['-created_time'],
            },
        ),
    ]